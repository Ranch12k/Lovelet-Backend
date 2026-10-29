from django.urls import path
from .views import NotificationPreferenceView, NotificationHistoryView

urlpatterns = [
    path('preferences/', NotificationPreferenceView.as_view(), name='notification_preferences'),
    path('history/', NotificationHistoryView.as_view(), name='notification_history'),
]
