from rest_framework import serializers
from .models import TemplateCategory, Template


class TemplateCategorySerializer(serializers.ModelSerializer):
    template_count = serializers.IntegerField(source='templates.count', read_only=True)

    class Meta:
        model = TemplateCategory
        fields = ['id', 'name', 'slug', 'icon', 'description', 'sort_order', 'template_count']


class TemplateListSerializer(serializers.ModelSerializer):
    category = TemplateCategorySerializer(read_only=True)

    class Meta:
        model = Template
        fields = [
            'id', 'title', 'slug', 'tagline', 'description', 'thumbnail_url',
            'envelope_theme', 'envelope_seal_text', 'background_style',
            'is_featured', 'is_free', 'category', 'created_at'
        ]


class TemplateDetailSerializer(serializers.ModelSerializer):
    category = TemplateCategorySerializer(read_only=True)

    class Meta:
        model = Template
        fields = [
            'id', 'title', 'slug', 'tagline', 'description', 'thumbnail_url',
            'envelope_theme', 'envelope_seal_text', 'background_style', 'music_url',
            'is_featured', 'is_free', 'category', 'pages_data', 'created_at', 'updated_at'
        ]
