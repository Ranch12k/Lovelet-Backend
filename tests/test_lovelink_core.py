import pytest
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from apps.templates_gallery.models import TemplateCategory, Template
from apps.experiences.models import Experience, ExperienceAccessSettings, ExperiencePage, ContentBlock
from apps.interactions.models import Question, Response as InteractionResponse
from apps.notifications.models import EmailNotification


@pytest.mark.django_db
class TestLoveLinkCore:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='romeo@example.com',
            email='romeo@example.com',
            first_name='Romeo',
            password='Password123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        anon_client = APIClient()
        res = anon_client.post('/api/v1/auth/register/', {
            'name': 'Juliet',
            'email': 'juliet@example.com',
            'password': 'SecretLove123!'
        })
        assert res.status_code == 201
        assert 'token' in res.data
        assert res.data['user']['email'] == 'juliet@example.com'

    def test_user_login(self):
        anon_client = APIClient()
        res = anon_client.post('/api/v1/auth/login/', {
            'email': 'romeo@example.com',
            'password': 'Password123!'
        })
        assert res.status_code == 200
        assert 'token' in res.data

    def test_template_cloning_into_experience(self):
        cat = TemplateCategory.objects.create(name='Proposals', slug='proposals')
        tpl = Template.objects.create(
            category=cat,
            title='Valentine Proposal',
            slug='valentine-proposal',
            pages_data=[
                {
                    'page_number': 1,
                    'title': 'Letter',
                    'blocks': [
                        {'block_type': 'heading', 'sort_order': 1, 'config': {'title': 'My Heart'}},
                        {'block_type': 'yes_no_question', 'sort_order': 2, 'config': {'prompt': 'Will you marry me?'}}
                    ]
                }
            ]
        )

        res = self.client.post(f'/api/v1/templates/{tpl.slug}/clone/')
        assert res.status_code == 201
        exp_id = res.data['experience_id']

        exp = Experience.objects.get(id=exp_id)
        assert exp.user == self.user
        assert exp.pages.count() == 1
        assert exp.pages.first().blocks.count() == 2
        assert exp.questions.count() == 1

    def test_experience_password_protection_and_unlock(self):
        exp = Experience.objects.create(
            user=self.user,
            title='Secret Love Note',
            status='published'
        )
        ExperienceAccessSettings.objects.create(
            experience=exp,
            is_password_protected=True,
            password_hash=make_password('rosebud')
        )

        anon_client = APIClient()
        # Initial request should be locked
        res = anon_client.get(f'/api/v1/experiences/public/{exp.slug}/')
        assert res.status_code == 200
        assert res.data['is_password_protected'] is True
        assert len(res.data['pages']) == 0

        # Attempt unlock with wrong password
        res_fail = anon_client.post(f'/api/v1/experiences/public/{exp.slug}/unlock/', {'password': 'wrong'})
        assert res_fail.status_code == 403

        # Attempt unlock with correct password
        res_ok = anon_client.post(f'/api/v1/experiences/public/{exp.slug}/unlock/', {'password': 'rosebud'})
        assert res_ok.status_code == 200
        assert res_ok.data['unlocked'] is True
        viewer_token = res_ok.data['viewer_token']

        # Request with viewer token should return full pages
        res_unlocked = anon_client.get(
            f'/api/v1/experiences/public/{exp.slug}/',
            HTTP_X_VIEWER_TOKEN=viewer_token
        )
        assert res_unlocked.status_code == 200
        assert res_unlocked.data.get('is_unlocked') is True

    def test_yes_no_response_and_email_notification(self):
        exp = Experience.objects.create(
            user=self.user,
            title='Proposal Question',
            status='published'
        )
        ExperienceAccessSettings.objects.create(
            experience=exp,
            allow_change_answer=True,
            notify_on_response=True
        )
        question = Question.objects.create(
            experience=exp,
            prompt="Will you be my Valentine? ❤️",
            yes_label="YES ❤️",
            no_label="NO 🙈",
            yes_message="Hooray! ❤️"
        )

        anon_client = APIClient()
        res = anon_client.post(f'/api/v1/experiences/public/{exp.slug}/respond/', {
            'answer': 'YES ❤️',
            'respondent_token': 'test-session-123'
        })
        assert res.status_code == 201
        assert res.data['is_yes'] is True
        assert res.data['reaction_message'] == "Hooray! ❤️"

        # Check response stored in DB
        db_resp = InteractionResponse.objects.filter(experience=exp).first()
        assert db_resp is not None
        assert db_resp.answer == 'YES ❤️'

        # Check EmailNotification generated
        notification = EmailNotification.objects.filter(response=db_resp).first()
        assert notification is not None
        assert notification.recipient_email == self.user.email
        assert notification.status == 'sent'
