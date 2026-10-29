from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import TemplateCategory, Template
from .serializers import TemplateCategorySerializer, TemplateListSerializer, TemplateDetailSerializer
from apps.experiences.models import Experience, ExperiencePage, ContentBlock, ExperienceAccessSettings
from apps.interactions.models import Question


class TemplateCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = TemplateCategory.objects.all().order_by('sort_order', 'name')
    serializer_class = TemplateCategorySerializer
    pagination_class = None


class TemplateListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TemplateListSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Template.objects.select_related('category').all()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(description__icontains=search)
        featured = self.request.query_params.get('featured')
        if featured in ('1', 'true', 'True'):
            qs = qs.filter(is_featured=True)
        return qs


class TemplateDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Template.objects.select_related('category').all()
    serializer_class = TemplateDetailSerializer
    lookup_field = 'slug'


class TemplateCloneView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, slug):
        template = get_object_or_404(Template, slug=slug)
        user = request.user

        # Create new experience based on template
        experience = Experience.objects.create(
            user=user,
            template=template,
            title=f"{template.title} (Personalized)",
            envelope_theme=template.envelope_theme,
            envelope_seal_text=template.envelope_seal_text,
            background_style=template.background_style,
            music_url=template.music_url,
            status='draft'
        )

        ExperienceAccessSettings.objects.create(
            experience=experience,
            is_password_protected=False,
            allow_change_answer=True,
            notify_on_response=True
        )

        # Clone pages and blocks
        pages_data = template.pages_data or []
        for p_idx, page_info in enumerate(pages_data, start=1):
            page = ExperiencePage.objects.create(
                experience=experience,
                page_number=page_info.get('page_number', p_idx),
                title=page_info.get('title', f"Page {p_idx}"),
                transition_effect=page_info.get('transition_effect', 'fade'),
                background_color=page_info.get('background_color', '')
            )

            blocks = page_info.get('blocks', [])
            for b_idx, block_info in enumerate(blocks, start=1):
                block_type = block_info.get('block_type', 'text')
                config = block_info.get('config', {})
                block = ContentBlock.objects.create(
                    page=page,
                    block_type=block_type,
                    sort_order=block_info.get('sort_order', b_idx),
                    config=config
                )

                # If this is an interactive question, create a Question record
                if block_type == 'yes_no_question':
                    Question.objects.create(
                        experience=experience,
                        block_id=str(block.id),
                        prompt=config.get('prompt', 'Will you be my Valentine? ❤️'),
                        yes_label=config.get('yes_label', 'YES ❤️'),
                        no_label=config.get('no_label', 'NO 🙈'),
                        yes_message=config.get('yes_message', 'You made my day! ❤️'),
                        no_message=config.get('no_message', 'I understand and care for you. ❤️'),
                    )

        return Response({
            'message': 'Template cloned successfully into your workspace!',
            'experience_id': str(experience.id),
            'slug': experience.slug
        }, status=status.HTTP_201_CREATED)
