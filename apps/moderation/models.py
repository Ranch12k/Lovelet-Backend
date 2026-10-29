import uuid
from django.db import models
from apps.experiences.models import Experience


class AbuseReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed & Safe'),
        ('dismissed', 'Dismissed'),
        ('takedown', 'Taken Down'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='abuse_reports')
    reason = models.CharField(max_length=150)
    details = models.TextField(blank=True)
    reporter_ip_hash = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report for {self.experience.title} [{self.status}]"
