from django.urls import path
from .views import TemplateCategoryListView, TemplateListView, TemplateDetailView, TemplateCloneView

urlpatterns = [
    path('categories/', TemplateCategoryListView.as_view(), name='template_categories'),
    path('', TemplateListView.as_view(), name='template_list'),
    path('<slug:slug>/', TemplateDetailView.as_view(), name='template_detail'),
    path('<slug:slug>/clone/', TemplateCloneView.as_view(), name='template_clone'),
]
