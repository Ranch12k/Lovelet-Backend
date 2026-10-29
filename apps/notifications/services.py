import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailNotification, NotificationPreference

logger = logging.getLogger(__name__)


def send_response_notification(response):
    """
    Sends an email notification to the creator of the experience when a recipient responds.
    Strictly uses the creator's verified account email.
    """
    experience = response.experience
    creator = experience.user

    # Check creator's notification preferences
    pref, _ = NotificationPreference.objects.get_or_create(user=creator)
    if not pref.email_on_response:
        logger.info(f"User {creator.email} has disabled response notifications.")
        return None

    # Check access settings toggle
    if hasattr(experience, 'access_settings') and not experience.access_settings.notify_on_response:
        logger.info(f"Experience {experience.title} has disabled response notifications.")
        return None

    subject = f"Someone responded to your LoveLink: {experience.title} ❤️"
    
    answer_display = response.answer
    prompt_display = response.question.prompt if response.question else "Question"
    
    plain_message = f"""Hello {creator.first_name or creator.username},

Your special person has responded to your LoveLink experience!

Experience: {experience.title}
Question: {prompt_display}
Answer: {answer_display}
Submitted: {response.created_at.strftime('%B %d, %Y at %I:%M %p UTC')}

Open your dashboard to view the full details:
{settings.PUBLIC_APP_URL}/dashboard/responses

With love,
The LoveLink Team
"""

    notification = EmailNotification.objects.create(
        response=response,
        recipient_email=creator.email,
        subject=subject,
        body=plain_message,
        status='pending'
    )

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[creator.email],
            fail_silently=False,
        )
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        logger.info(f"Response notification sent successfully to {creator.email}")
    except Exception as e:
        logger.error(f"Failed to send response notification to {creator.email}: {e}")
        notification.status = 'failed'
        notification.error_message = str(e)
        notification.save()

    return notification
