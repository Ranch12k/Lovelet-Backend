from rest_framework import serializers
from .models import NotificationPreference, EmailNotification


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['email_on_response', 'email_on_milestone', 'updated_at']


class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = ['id', 'recipient_email', 'subject', 'status', 'error_message', 'sent_at', 'created_at']
