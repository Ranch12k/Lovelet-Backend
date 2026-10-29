from rest_framework import serializers
from .models import Experience, ExperienceAccessSettings, ExperiencePage, ContentBlock
from apps.interactions.models import Question


class ContentBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentBlock
        fields = ['id', 'block_type', 'sort_order', 'config']


class ExperiencePageSerializer(serializers.ModelSerializer):
    blocks = ContentBlockSerializer(many=True, read_only=True)

    class Meta:
        model = ExperiencePage
        fields = ['id', 'page_number', 'title', 'transition_effect', 'background_color', 'blocks']


class ExperienceAccessSettingsSerializer(serializers.ModelSerializer):
    is_password_set = serializers.SerializerMethodField()

    class Meta:
        model = ExperienceAccessSettings
        fields = ['is_password_protected', 'allow_change_answer', 'notify_on_response', 'is_password_set']

    def get_is_password_set(self, obj):
        return bool(obj.password_hash)


class ExperienceListSerializer(serializers.ModelSerializer):
    response_count = serializers.IntegerField(source='responses.count', read_only=True)
    is_password_protected = serializers.BooleanField(source='access_settings.is_password_protected', read_only=True)

    class Meta:
        model = Experience
        fields = [
            'id', 'title', 'slug', 'status', 'envelope_theme', 'envelope_seal_text',
            'background_style', 'view_count', 'response_count', 'is_password_protected',
            'expires_at', 'response_deadline', 'created_at', 'updated_at'
        ]


class ExperienceDetailSerializer(serializers.ModelSerializer):
    pages = ExperiencePageSerializer(many=True, read_only=True)
    access_settings = ExperienceAccessSettingsSerializer(read_only=True)
    response_count = serializers.IntegerField(source='responses.count', read_only=True)

    class Meta:
        model = Experience
        fields = [
            'id', 'title', 'slug', 'status', 'envelope_theme', 'envelope_seal_text',
            'envelope_to', 'envelope_from', 'background_style', 'music_url',
            'expires_at', 'response_deadline', 'custom_share_message', 'view_count',
            'response_count', 'access_settings', 'pages', 'created_at', 'updated_at'
        ]


class PublicExperienceSerializer(serializers.ModelSerializer):
    pages = ExperiencePageSerializer(many=True, read_only=True)
    is_password_protected = serializers.BooleanField(source='access_settings.is_password_protected', read_only=True)

    class Meta:
        model = Experience
        fields = [
            'title', 'slug', 'envelope_theme', 'envelope_seal_text', 'envelope_to',
            'envelope_from', 'background_style', 'music_url', 'expires_at',
            'is_password_protected', 'pages'
        ]
