import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.templates_gallery.models import TemplateCategory, Template
from apps.experiences.models import Experience
from apps.interactions.models import Response as InteractionResponse
from apps.notifications.models import EmailNotification


@pytest.mark.django_db
class TestE2EFullJourney:
    def test_complete_creator_to_recipient_journey(self):
        # 1. Register a new user
        client = APIClient()
        reg_res = client.post('/api/v1/auth/register/', {
            'name': 'Sarah Connor',
            'email': 'sarah@example.com',
            'password': 'PassSecure2026!'
        })
        assert reg_res.status_code == 201
        token = reg_res.data['token']
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # 2. Pick a proposal template from gallery
        cat = TemplateCategory.objects.create(name='Proposals', slug='proposals')
        tpl = Template.objects.create(
            category=cat,
            title='Valentine Proposal',
            slug='valentine-proposal',
            envelope_theme='rose_gold',
            envelope_seal_text='BE MINE',
            background_style='romantic_gradient',
            pages_data=[
                {
                    'page_number': 1,
                    'title': 'The Envelope',
                    'blocks': [{'block_type': 'envelope', 'sort_order': 1, 'config': {'seal_text': 'BE MINE'}}]
                },
                {
                    'page_number': 2,
                    'title': 'The Question',
                    'blocks': [{
                        'block_type': 'yes_no_question',
                        'sort_order': 1,
                        'config': {
                            'prompt': 'Will you be my Valentine? ❤️',
                            'yes_label': 'YES ❤️',
                            'no_label': 'NO 🙈',
                            'yes_message': 'You made my whole world brighter! ❤️'
                        }
                    }]
                }
            ]
        )

        # Clone template into user workspace
        clone_res = client.post(f'/api/v1/templates/{tpl.slug}/clone/')
        assert clone_res.status_code == 201
        exp_id = clone_res.data['experience_id']

        # 3. Configure password protection and custom settings
        put_res = client.put(f'/api/v1/experiences/{exp_id}/', {
            'title': 'Secret Note for Kyle',
            'is_password_protected': True,
            'password': 'secretlovepass',
            'notify_on_response': True,
            'allow_change_answer': True
        })
        assert put_res.status_code == 200

        # 4. Publish experience
        pub_res = client.post(f'/api/v1/experiences/{exp_id}/publish/')
        assert pub_res.status_code == 200
        assert pub_res.data['is_published'] is True
        slug = pub_res.data['slug']

        # 5. Open link in a separate anonymous recipient context
        recipient_client = APIClient()

        # Recipient attempts to view - should be password gated
        view_gated = recipient_client.get(f'/api/v1/experiences/public/{slug}/')
        assert view_gated.status_code == 200
        assert view_gated.data['is_password_protected'] is True
        assert len(view_gated.data['pages']) == 0

        # Recipient enters wrong password
        fail_unlock = recipient_client.post(f'/api/v1/experiences/public/{slug}/unlock/', {
            'password': 'incorrect_password'
        })
        assert fail_unlock.status_code == 403

        # Recipient enters correct password
        ok_unlock = recipient_client.post(f'/api/v1/experiences/public/{slug}/unlock/', {
            'password': 'secretlovepass'
        })
        assert ok_unlock.status_code == 200
        assert ok_unlock.data['unlocked'] is True
        viewer_token = ok_unlock.data['viewer_token']

        # Recipient views unlocked experience with viewer token
        view_unlocked = recipient_client.get(
            f'/api/v1/experiences/public/{slug}/',
            HTTP_X_VIEWER_TOKEN=viewer_token
        )
        assert view_unlocked.status_code == 200
        assert view_unlocked.data['is_unlocked'] is True
        assert len(view_unlocked.data['pages']) == 2

        # 6. Recipient responds "YES ❤️" with a follow-up note
        respond_res = recipient_client.post(f'/api/v1/experiences/public/{slug}/respond/', {
            'answer': 'YES ❤️',
            'respondent_token': 'browser-kyle-session-token',
            'followup_answer': 'I cannot wait for our date! ❤️'
        })
        assert respond_res.status_code == 201
        assert respond_res.data['is_yes'] is True
        assert 'brighter' in respond_res.data['reaction_message']

        # 7. Verify response in creator dashboard
        dash_res = client.get('/api/v1/responses/')
        assert dash_res.status_code == 200
        assert len(dash_res.data) == 1
        assert dash_res.data[0]['answer'] == 'YES ❤️'
        assert dash_res.data[0]['followup_answer'] == 'I cannot wait for our date! ❤️'

        # 8. Verify email notification generated for creator
        email_notif = EmailNotification.objects.filter(recipient_email='sarah@example.com').first()
        assert email_notif is not None
        assert email_notif.status == 'sent'
        assert 'Someone responded to your LoveLink' in email_notif.subject
        assert 'YES ❤️' in email_notif.body
