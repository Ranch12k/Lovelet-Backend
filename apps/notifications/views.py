from rest_framework import views, permissions
from rest_framework.response import Response
from .models import NotificationPreference, EmailNotification
from .serializers import NotificationPreferenceSerializer, EmailNotificationSerializer


class NotificationPreferenceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pref, _ = NotificationPreference.objects.get_or_create(user=request.user)
        return Response(NotificationPreferenceSerializer(pref).data)

    def put(self, request):
        pref, _ = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class NotificationHistoryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = EmailNotification.objects.filter(
            response__experience__user=request.user
        ).order_by('-created_at')[:50]
        return Response(EmailNotificationSerializer(notifications, many=True).data)
