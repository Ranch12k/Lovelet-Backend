from django.urls import path
from .views import (
    ExperienceListCreateView,
    ExperienceDetailView,
    ExperienceDuplicateView,
    ExperiencePublishToggleView,
    ExperienceRegenerateSlugView,
    PageCreateView,
    PageDetailView,
    BlockCreateView,
    BlockDetailView,
    PublicExperienceView,
    PublicExperienceUnlockView,
    PublicExperienceRespondView,
    PublicExperienceVisitView
)

urlpatterns = [
    # Creator Experience CRUD
    path('', ExperienceListCreateView.as_view(), name='experience_list_create'),
    path('<uuid:pk>/', ExperienceDetailView.as_view(), name='experience_detail'),
    path('<uuid:pk>/duplicate/', ExperienceDuplicateView.as_view(), name='experience_duplicate'),
    path('<uuid:pk>/publish/', ExperiencePublishToggleView.as_view(), name='experience_publish_toggle'),
    path('<uuid:pk>/regenerate-slug/', ExperienceRegenerateSlugView.as_view(), name='experience_regenerate_slug'),

    # Pages & Blocks visual editor
    path('<uuid:pk>/pages/', PageCreateView.as_view(), name='page_create'),
    path('<uuid:pk>/pages/<uuid:page_id>/', PageDetailView.as_view(), name='page_detail'),
    path('<uuid:pk>/pages/<uuid:page_id>/blocks/', BlockCreateView.as_view(), name='block_create'),
    path('<uuid:pk>/pages/<uuid:page_id>/blocks/<uuid:block_id>/', BlockDetailView.as_view(), name='block_detail'),

    # Public Recipient endpoints
    path('public/<str:slug>/', PublicExperienceView.as_view(), name='public_experience'),
    path('public/<str:slug>/unlock/', PublicExperienceUnlockView.as_view(), name='public_experience_unlock'),
    path('public/<str:slug>/respond/', PublicExperienceRespondView.as_view(), name='public_experience_respond'),
    path('public/<str:slug>/visit/', PublicExperienceVisitView.as_view(), name='public_experience_visit'),
]
