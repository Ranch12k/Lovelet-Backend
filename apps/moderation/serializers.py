from rest_framework import serializers
from .models import AbuseReport


class AbuseReportSerializer(serializers.ModelSerializer):
    experience_title = serializers.CharField(source='experience.title', read_only=True)
    experience_slug = serializers.CharField(source='experience.slug', read_only=True)

    class Meta:
        model = AbuseReport
        fields = [
            'id', 'experience', 'experience_title', 'experience_slug',
            'reason', 'details', 'status', 'admin_notes', 'created_at'
        ]
        read_only_fields = ['status', 'admin_notes', 'created_at']
