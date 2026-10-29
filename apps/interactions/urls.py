from django.urls import path
from .views import ResponseListView, ResponseDetailView, DashboardStatsView

urlpatterns = [
    path('responses/', ResponseListView.as_view(), name='response_list'),
    path('responses/<uuid:pk>/', ResponseDetailView.as_view(), name='response_detail'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
]
