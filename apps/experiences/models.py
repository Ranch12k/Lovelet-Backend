import uuid
import secrets
from django.db import models
from django.contrib.auth.models import User
from apps.templates_gallery.models import Template


def generate_secret_slug():
    return secrets.token_urlsafe(8)


class Experience(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True, related_name='experiences')
    title = models.CharField(max_length=200, default='My Love Letter')
    slug = models.CharField(max_length=64, unique=True, db_index=True, default=generate_secret_slug)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Visual Styling
    envelope_theme = models.CharField(max_length=50, default='rose_gold')
    envelope_seal_text = models.CharField(max_length=50, default='LOVE')
    envelope_to = models.CharField(max_length=150, blank=True, default='My Beloved')
    envelope_from = models.CharField(max_length=150, blank=True)
    background_style = models.CharField(max_length=50, default='romantic_gradient')
    music_url = models.CharField(max_length=500, blank=True)
    
    # Timing & Expiration
    expires_at = models.DateTimeField(null=True, blank=True)
    response_deadline = models.DateTimeField(null=True, blank=True)
    custom_share_message = models.TextField(blank=True, default='Hey ❤️ I made something special for you. Open it when you have a moment.')
    view_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.slug})"


class ExperienceAccessSettings(models.Model):
    experience = models.OneToOneField(Experience, on_delete=models.CASCADE, related_name='access_settings')
    is_password_protected = models.BooleanField(default=False)
    password_hash = models.CharField(max_length=255, blank=True)
    allow_change_answer = models.BooleanField(default=True)
    notify_on_response = models.BooleanField(default=True)

    def __str__(self):
        return f"AccessSettings for {self.experience.title}"


class ExperiencePage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='pages')
    page_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=150, blank=True, default='Page')
    transition_effect = models.CharField(max_length=50, default='fade')  # fade, slide, flip, zoom
    background_color = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['page_number']

    def __str__(self):
        return f"{self.experience.title} - Page {self.page_number}"


class ContentBlock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.ForeignKey(ExperiencePage, on_delete=models.CASCADE, related_name='blocks')
    block_type = models.CharField(max_length=50)
    sort_order = models.PositiveIntegerField(default=0)
    config = models.JSONField(default=dict)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"{self.block_type} ({self.sort_order}) on {self.page}"


class ExperienceAnalytics(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='analytics')
    ip_hash = models.CharField(max_length=64, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
