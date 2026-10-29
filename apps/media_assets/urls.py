from django.urls import path
from .views import MediaAssetListUploadView, MediaAssetDetailView

urlpatterns = [
    path('', MediaAssetListUploadView.as_view(), name='media_list_upload'),
    path('<uuid:pk>/', MediaAssetDetailView.as_view(), name='media_detail'),
]
