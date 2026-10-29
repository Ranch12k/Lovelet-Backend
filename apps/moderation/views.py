import hashlib
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import AbuseReport
from .serializers import AbuseReportSerializer
from apps.experiences.models import Experience
from apps.interactions.models import Response as InteractionResponse


class ReportAbuseView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        slug = request.data.get('slug')
        reason = request.data.get('reason', 'Inappropriate content')
        details = request.data.get('details', '')

        experience = get_object_or_404(Experience, slug=slug)
        ip = request.META.get('REMOTE_ADDR', '')
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16] if ip else ''

        report = AbuseReport.objects.create(
            experience=experience,
            reason=reason,
            details=details,
            reporter_ip_hash=ip_hash
        )
        return Response({'message': 'Report received. Thank you for keeping LoveLink safe.'}, status=status.HTTP_201_CREATED)


class AdminReportsListView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        reports = AbuseReport.objects.select_related('experience').all()
        return Response(AbuseReportSerializer(reports, many=True).data)


class AdminExperienceTakedownView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        experience = get_object_or_404(Experience, id=pk)
        experience.status = 'archived'
        experience.save()

        AbuseReport.objects.filter(experience=experience).update(status='takedown')
        return Response({'message': f"Experience '{experience.title}' has been taken down and archived."})


class AdminPlatformStatsView(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_users = User.objects.count()
        total_experiences = Experience.objects.count()
        published_experiences = Experience.objects.filter(status='published').count()
        total_responses = InteractionResponse.objects.count()
        total_visits = sum(e.view_count for e in Experience.objects.all())
        pending_reports = AbuseReport.objects.filter(status='pending').count()

        return Response({
            'total_users': total_users,
            'total_experiences': total_experiences,
            'published_experiences': published_experiences,
            'total_responses': total_responses,
            'total_visits': total_visits,
            'pending_reports': pending_reports
        })
