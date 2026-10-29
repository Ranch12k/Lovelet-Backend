from django.urls import path
from .views import ReportAbuseView, AdminReportsListView, AdminExperienceTakedownView, AdminPlatformStatsView

urlpatterns = [
    path('report/', ReportAbuseView.as_view(), name='moderation_report'),
    path('admin/reports/', AdminReportsListView.as_view(), name='admin_reports'),
    path('admin/experiences/<uuid:pk>/takedown/', AdminExperienceTakedownView.as_view(), name='admin_takedown'),
    path('admin/platform-stats/', AdminPlatformStatsView.as_view(), name='admin_platform_stats'),
]
