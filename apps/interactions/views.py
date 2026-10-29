from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Response as InteractionResponse
from .serializers import ResponseSerializer
from apps.experiences.models import Experience


class ResponseListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_experiences = Experience.objects.filter(user=request.user)
        responses = InteractionResponse.objects.filter(experience__in=user_experiences).select_related('experience', 'question')
        
        experience_id = request.query_params.get('experience_id')
        if experience_id:
            responses = responses.filter(experience_id=experience_id)
            
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data)


class ResponseDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        user_experiences = Experience.objects.filter(user=request.user)
        resp = get_object_or_404(InteractionResponse, id=pk, experience__in=user_experiences)
        resp.delete()
        return Response({'message': 'Response deleted successfully.'})


class DashboardStatsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_experiences = Experience.objects.filter(user=request.user)
        total_experiences = user_experiences.count()
        published_count = user_experiences.filter(status='published').count()
        draft_count = user_experiences.filter(status='draft').count()

        total_views = sum(exp.view_count for exp in user_experiences)
        responses = InteractionResponse.objects.filter(experience__in=user_experiences)
        total_responses = responses.count()

        yes_count = sum(1 for r in responses if r.answer.upper().startswith('YES'))
        no_count = total_responses - yes_count

        recent_responses = ResponseSerializer(responses.select_related('experience', 'question')[:5], many=True).data

        return Response({
            'total_experiences': total_experiences,
            'published_count': published_count,
            'draft_count': draft_count,
            'total_views': total_views,
            'total_responses': total_responses,
            'yes_count': yes_count,
            'no_count': no_count,
            'recent_responses': recent_responses
        })
