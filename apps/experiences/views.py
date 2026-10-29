import secrets
import hashlib
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from rest_framework import status, views, permissions, generics
from rest_framework.response import Response

from .models import Experience, ExperienceAccessSettings, ExperiencePage, ContentBlock, ExperienceAnalytics
from .serializers import (
    ExperienceListSerializer,
    ExperienceDetailSerializer,
    PublicExperienceSerializer,
    ExperiencePageSerializer,
    ContentBlockSerializer
)
from apps.interactions.models import Question, Response as InteractionResponse
from apps.notifications.services import send_response_notification


class ExperienceListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        experiences = Experience.objects.filter(user=request.user).prefetch_related('responses')
        serializer = ExperienceListSerializer(experiences, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        title = request.data.get('title', 'My Love Letter')
        envelope_theme = request.data.get('envelope_theme', 'rose_gold')
        background_style = request.data.get('background_style', 'romantic_gradient')

        experience = Experience.objects.create(
            user=request.user,
            title=title,
            envelope_theme=envelope_theme,
            background_style=background_style,
            status='draft'
        )

        ExperienceAccessSettings.objects.create(
            experience=experience,
            is_password_protected=False,
            allow_change_answer=True,
            notify_on_response=True
        )

        # Create default Page 1 with Envelope block
        page1 = ExperiencePage.objects.create(
            experience=experience,
            page_number=1,
            title='The Envelope',
            transition_effect='fade'
        )
        ContentBlock.objects.create(
            page=page1,
            block_type='envelope',
            sort_order=1,
            config={
                'to_name': 'My Beloved',
                'from_name': request.user.first_name or request.user.username,
                'seal_text': 'LOVE',
                'teaser': 'A secret waiting for you inside... tap to open ❤️',
                'theme': envelope_theme
            }
        )

        # Create default Page 2 with Letter text
        page2 = ExperiencePage.objects.create(
            experience=experience,
            page_number=2,
            title='My Letter',
            transition_effect='slide'
        )
        ContentBlock.objects.create(
            page=page2,
            block_type='heading',
            sort_order=1,
            config={
                'title': 'Thinking Of You',
                'subtitle': 'Every single day feels brighter with you in it.'
            }
        )
        ContentBlock.objects.create(
            page=page2,
            block_type='text',
            sort_order=2,
            config={
                'content': 'I just wanted to take a moment to write down how much you mean to me.\n\nThank you for every smile, every quiet moment, and all the love you bring into my life.',
                'style': 'serif',
                'align': 'center'
            }
        )

        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExperienceDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Experience, id=pk, user=user)

    def get(self, request, pk):
        experience = self.get_object(pk, request.user)
        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    @transaction.atomic
    def put(self, request, pk):
        experience = self.get_object(pk, request.user)
        data = request.data

        # Update experience core fields
        for field in ['title', 'envelope_theme', 'envelope_seal_text', 'envelope_to', 'envelope_from',
                      'background_style', 'music_url', 'custom_share_message', 'expires_at', 'response_deadline']:
            if field in data:
                setattr(experience, field, data[field])
        experience.save()

        # Update access settings
        access_settings, _ = ExperienceAccessSettings.objects.get_or_create(experience=experience)
        if 'is_password_protected' in data:
            access_settings.is_password_protected = bool(data['is_password_protected'])
        if 'password' in data and data['password']:
            access_settings.password_hash = make_password(data['password'])
            access_settings.is_password_protected = True
        elif data.get('remove_password'):
            access_settings.password_hash = ''
            access_settings.is_password_protected = False

        if 'allow_change_answer' in data:
            access_settings.allow_change_answer = bool(data['allow_change_answer'])
        if 'notify_on_response' in data:
            access_settings.notify_on_response = bool(data['notify_on_response'])

        access_settings.save()

        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def delete(self, request, pk):
        experience = self.get_object(pk, request.user)
        experience.delete()
        return Response({'message': 'Experience deleted successfully.'})


class ExperienceDuplicateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        orig = get_object_or_404(Experience, id=pk, user=request.user)

        new_exp = Experience.objects.create(
            user=request.user,
            template=orig.template,
            title=f"{orig.title} (Copy)",
            envelope_theme=orig.envelope_theme,
            envelope_seal_text=orig.envelope_seal_text,
            envelope_to=orig.envelope_to,
            envelope_from=orig.envelope_from,
            background_style=orig.background_style,
            music_url=orig.music_url,
            custom_share_message=orig.custom_share_message,
            status='draft'
        )

        ExperienceAccessSettings.objects.create(
            experience=new_exp,
            is_password_protected=orig.access_settings.is_password_protected,
            password_hash=orig.access_settings.password_hash,
            allow_change_answer=orig.access_settings.allow_change_answer,
            notify_on_response=orig.access_settings.notify_on_response
        )

        for page in orig.pages.all():
            new_page = ExperiencePage.objects.create(
                experience=new_exp,
                page_number=page.page_number,
                title=page.title,
                transition_effect=page.transition_effect,
                background_color=page.background_color
            )
            for block in page.blocks.all():
                new_block = ContentBlock.objects.create(
                    page=new_page,
                    block_type=block.block_type,
                    sort_order=block.sort_order,
                    config=block.config
                )
                if block.block_type == 'yes_no_question':
                    orig_q = orig.questions.filter(block_id=str(block.id)).first()
                    if orig_q:
                        Question.objects.create(
                            experience=new_exp,
                            block_id=str(new_block.id),
                            prompt=orig_q.prompt,
                            yes_label=orig_q.yes_label,
                            no_label=orig_q.no_label,
                            yes_message=orig_q.yes_message,
                            no_message=orig_q.no_message
                        )

        return Response(ExperienceDetailSerializer(new_exp).data, status=status.HTTP_201_CREATED)


class ExperiencePublishToggleView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        new_status = 'published' if experience.status != 'published' else 'draft'
        experience.status = new_status
        experience.save()
        return Response({
            'status': experience.status,
            'is_published': experience.status == 'published',
            'slug': experience.slug,
            'share_url': f"{request.build_absolute_uri('/')}l/{experience.slug}"
        })


class ExperienceRegenerateSlugView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        experience.slug = secrets.token_urlsafe(8)
        experience.save()
        return Response({
            'slug': experience.slug,
            'share_url': f"{request.build_absolute_uri('/')}l/{experience.slug}"
        })


# --- Page & Block Management ---

class PageCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        last_page = experience.pages.order_by('-page_number').first()
        next_num = (last_page.page_number + 1) if last_page else 1

        page = ExperiencePage.objects.create(
            experience=experience,
            page_number=next_num,
            title=request.data.get('title', f"Page {next_num}"),
            transition_effect=request.data.get('transition_effect', 'slide')
        )
        return Response(ExperiencePageSerializer(page).data, status=status.HTTP_201_CREATED)


class PageDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, page_id):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        page = get_object_or_404(ExperiencePage, id=page_id, experience=experience)

        for field in ['title', 'transition_effect', 'background_color', 'page_number']:
            if field in request.data:
                setattr(page, field, request.data[field])
        page.save()
        return Response(ExperiencePageSerializer(page).data)

    def delete(self, request, pk, page_id):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        page = get_object_or_404(ExperiencePage, id=page_id, experience=experience)
        page.delete()
        return Response({'message': 'Page deleted.'})


class BlockCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk, page_id):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        page = get_object_or_404(ExperiencePage, id=page_id, experience=experience)

        block_type = request.data.get('block_type', 'text')
        config = request.data.get('config', {})
        last_block = page.blocks.order_by('-sort_order').first()
        sort_order = (last_block.sort_order + 1) if last_block else 1

        block = ContentBlock.objects.create(
            page=page,
            block_type=block_type,
            sort_order=sort_order,
            config=config
        )

        if block_type == 'yes_no_question':
            Question.objects.create(
                experience=experience,
                block_id=str(block.id),
                prompt=config.get('prompt', 'Will you be my Valentine? ❤️'),
                yes_label=config.get('yes_label', 'YES ❤️'),
                no_label=config.get('no_label', 'NO 🙈'),
                yes_message=config.get('yes_message', 'You made me the happiest person! ❤️'),
                no_message=config.get('no_message', 'I understand and care for you. ❤️')
            )

        return Response(ContentBlockSerializer(block).data, status=status.HTTP_201_CREATED)


class BlockDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def put(self, request, pk, page_id, block_id):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        page = get_object_or_404(ExperiencePage, id=page_id, experience=experience)
        block = get_object_or_404(ContentBlock, id=block_id, page=page)

        if 'config' in request.data:
            block.config = request.data['config']
        if 'sort_order' in request.data:
            block.sort_order = request.data['sort_order']
        block.save()

        # Keep question model in sync if yes_no_question
        if block.block_type == 'yes_no_question':
            cfg = block.config
            question, _ = Question.objects.get_or_create(experience=experience, block_id=str(block.id))
            question.prompt = cfg.get('prompt', question.prompt)
            question.yes_label = cfg.get('yes_label', question.yes_label)
            question.no_label = cfg.get('no_label', question.no_label)
            question.yes_message = cfg.get('yes_message', question.yes_message)
            question.no_message = cfg.get('no_message', question.no_message)
            question.save()

        return Response(ContentBlockSerializer(block).data)

    def delete(self, request, pk, page_id, block_id):
        experience = get_object_or_404(Experience, id=pk, user=request.user)
        page = get_object_or_404(ExperiencePage, id=page_id, experience=experience)
        block = get_object_or_404(ContentBlock, id=block_id, page=page)
        Question.objects.filter(experience=experience, block_id=str(block.id)).delete()
        block.delete()
        return Response({'message': 'Block deleted.'})


# --- Public Recipient Experience Endpoints ---

class PublicExperienceView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        experience = get_object_or_404(
            Experience.objects.select_related('access_settings').prefetch_related('pages__blocks'),
            slug=slug
        )

        # Check if experience is published (allow creator to preview drafts)
        is_owner = request.user.is_authenticated and experience.user_id == request.user.id
        if experience.status != 'published' and not is_owner:
            return Response(
                {'detail': 'This experience is currently in draft mode or private.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check expiration
        if experience.expires_at and experience.expires_at < timezone.now() and not is_owner:
            return Response(
                {'detail': 'This LoveLink experience has expired.'},
                status=status.HTTP_410_GONE
            )

        access_settings = getattr(experience, 'access_settings', None)
        is_password_protected = access_settings and access_settings.is_password_protected

        # Check if recipient already unlocked via session header or token
        viewer_token = request.headers.get('X-Viewer-Token') or request.query_params.get('token')
        expected_token = hashlib.sha256(f"{experience.slug}-{access_settings.password_hash}".encode()).hexdigest() if is_password_protected else None

        is_unlocked = not is_password_protected or is_owner or (viewer_token and viewer_token == expected_token)

        if not is_unlocked:
            # Mask private content! Return only minimal teaser metadata
            return Response({
                'title': experience.title,
                'slug': experience.slug,
                'envelope_theme': experience.envelope_theme,
                'envelope_seal_text': experience.envelope_seal_text,
                'is_password_protected': True,
                'pages': []
            })

        # Return full content
        serializer = PublicExperienceSerializer(experience)
        data = serializer.data
        data['is_unlocked'] = True
        return Response(data)


class PublicExperienceUnlockView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, slug):
        experience = get_object_or_404(Experience.objects.select_related('access_settings'), slug=slug)
        access_settings = getattr(experience, 'access_settings', None)

        if not access_settings or not access_settings.is_password_protected:
            return Response({'message': 'This experience is not password protected.', 'unlocked': True})

        password = request.data.get('password', '')
        if not password:
            return Response({'detail': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(password, access_settings.password_hash):
            return Response({'detail': 'Incorrect secret password. Please try again!'}, status=status.HTTP_403_FORBIDDEN)

        # Issue secure viewer token
        viewer_token = hashlib.sha256(f"{experience.slug}-{access_settings.password_hash}".encode()).hexdigest()
        return Response({
            'message': 'Access granted! Unwrapping your special gift...',
            'unlocked': True,
            'viewer_token': viewer_token
        })


class PublicExperienceRespondView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request, slug):
        experience = get_object_or_404(Experience, slug=slug)
        answer = request.data.get('answer', '').strip()
        respondent_token = request.data.get('respondent_token', '').strip()
        followup_answer = request.data.get('followup_answer', '').strip()

        if not answer:
            return Response({'detail': 'Answer is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not respondent_token:
            respondent_token = secrets.token_urlsafe(16)

        # Get or create question reference
        question = experience.questions.first()
        if not question:
            question = Question.objects.create(
                experience=experience,
                prompt="Will you be mine?",
                yes_label="YES ❤️",
                no_label="NO 🙈"
            )

        access_settings = getattr(experience, 'access_settings', None)
        allow_change = access_settings.allow_change_answer if access_settings else True

        # Check existing response by this recipient
        existing = InteractionResponse.objects.filter(experience=experience, respondent_token=respondent_token).first()
        if existing and not allow_change:
            return Response({
                'detail': 'Your response has already been recorded and cannot be changed.',
                'already_recorded': True
            }, status=status.HTTP_409_CONFLICT)

        if existing:
            existing.answer = answer
            if followup_answer:
                existing.followup_answer = followup_answer
            existing.save()
            response_obj = existing
        else:
            response_obj = InteractionResponse.objects.create(
                experience=experience,
                question=question,
                respondent_token=respondent_token,
                answer=answer,
                followup_answer=followup_answer
            )

        # Trigger notification to creator
        send_response_notification(response_obj)

        # Determine reaction message
        is_yes = answer.upper().startswith('YES')
        reaction_message = question.yes_message if is_yes else question.no_message

        return Response({
            'message': 'Response submitted successfully!',
            'answer': answer,
            'reaction_message': reaction_message,
            'respondent_token': respondent_token,
            'is_yes': is_yes
        }, status=status.HTTP_201_CREATED)


class PublicExperienceVisitView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, slug):
        experience = get_object_or_404(Experience, slug=slug)
        experience.view_count += 1
        experience.save(update_fields=['view_count'])

        # Privacy-conscious hash of IP
        ip = request.META.get('REMOTE_ADDR', '')
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16] if ip else ''
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:250]

        ExperienceAnalytics.objects.create(
            experience=experience,
            ip_hash=ip_hash,
            user_agent=user_agent
        )

        return Response({'view_count': experience.view_count})
