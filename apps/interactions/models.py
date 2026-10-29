import uuid
from django.db import models
from apps.experiences.models import Experience


class Question(models.Model):
    QUESTION_TYPES = (
        ('yes_no', 'Yes / No Question'),
        ('choice', 'Multiple Choice'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='questions')
    block_id = models.CharField(max_length=64, blank=True)
    prompt = models.CharField(max_length=500, default='Will you be my Valentine? ❤️')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='yes_no')
    yes_label = models.CharField(max_length=100, default='YES ❤️')
    no_label = models.CharField(max_length=100, default='NO 🙈')
    yes_message = models.TextField(default='You just made my entire world brighter! I love you so much! ❤️')
    no_message = models.TextField(default='I appreciate your honesty, and my care for you remains endless. ❤️')
    followup_prompt = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prompt} ({self.experience.title})"


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=200)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.label


class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='responses')
    respondent_token = models.CharField(max_length=128, db_index=True)
    answer = models.CharField(max_length=255)
    followup_answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Response '{self.answer}' for {self.question.prompt}"
