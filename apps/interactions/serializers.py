from rest_framework import serializers
from .models import Question, QuestionOption, Response


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'label', 'sort_order']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'prompt', 'question_type', 'yes_label', 'no_label',
            'yes_message', 'no_message', 'followup_prompt', 'options'
        ]


class ResponseSerializer(serializers.ModelSerializer):
    experience_title = serializers.CharField(source='experience.title', read_only=True)
    question_prompt = serializers.CharField(source='question.prompt', read_only=True)

    class Meta:
        model = Response
        fields = [
            'id', 'experience', 'experience_title', 'question', 'question_prompt',
            'respondent_token', 'answer', 'followup_answer', 'created_at', 'updated_at'
        ]
