from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/templates/', include('apps.templates_gallery.urls')),
    path('api/v1/experiences/', include('apps.experiences.urls')),
    path('api/v1/', include('apps.interactions.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/media/', include('apps.media_assets.urls')),
    path('api/v1/moderation/', include('apps.moderation.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
