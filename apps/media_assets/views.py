import os
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MediaAsset
from .serializers import MediaAssetSerializer

ALLOWED_MIME_TYPES = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/webp': '.webp',
    'image/gif': '.gif',
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
USER_STORAGE_QUOTA = 50 * 1024 * 1024  # 50 MB


class MediaAssetListUploadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        assets = MediaAsset.objects.filter(user=request.user)
        total_used = sum(a.size_bytes for a in assets)
        serializer = MediaAssetSerializer(assets, many=True, context={'request': request})
        return Response({
            'assets': serializer.data,
            'total_used_bytes': total_used,
            'quota_bytes': USER_STORAGE_QUOTA,
            'percent_used': round((total_used / USER_STORAGE_QUOTA) * 100, 1) if USER_STORAGE_QUOTA else 0
        })

    def post(self, request):
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'detail': 'No file was provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if uploaded_file.size > MAX_FILE_SIZE:
            return Response({'detail': f'File exceeds maximum limit of {MAX_FILE_SIZE // (1024*1024)}MB.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check storage quota
        current_used = sum(a.size_bytes for a in MediaAsset.objects.filter(user=request.user))
        if current_used + uploaded_file.size > USER_STORAGE_QUOTA:
            return Response({'detail': 'Storage quota exceeded. Please remove existing media first.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate MIME type and image integrity with Pillow
        try:
            img = Image.open(uploaded_file)
            img.verify()  # Verify it is indeed a valid image
            # Reopen after verify
            uploaded_file.seek(0)
            img = Image.open(uploaded_file)
            width, height = img.size
            format_name = (img.format or 'JPEG').lower()
            mime_type = f"image/{format_name}"
            if format_name == 'jpg':
                mime_type = 'image/jpeg'
        except Exception:
            return Response({'detail': 'Invalid or corrupted image file.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create thumbnail
        thumbnail_file = None
        try:
            thumb_img = img.copy()
            thumb_img.thumbnail((400, 400), Image.Resampling.LANCZOS)
            thumb_io = io.BytesIO()
            save_format = 'JPEG' if img.format not in ['PNG', 'WEBP', 'GIF'] else img.format
            if save_format == 'JPEG' and thumb_img.mode in ('RGBA', 'P'):
                thumb_img = thumb_img.convert('RGB')
            thumb_img.save(thumb_io, format=save_format, quality=85)
            thumb_name = f"thumb_{uploaded_file.name}"
            thumbnail_file = ContentFile(thumb_io.getvalue(), name=thumb_name)
        except Exception:
            pass

        uploaded_file.seek(0)
        asset = MediaAsset.objects.create(
            user=request.user,
            file=uploaded_file,
            thumbnail=thumbnail_file,
            original_name=uploaded_file.name,
            mime_type=mime_type,
            size_bytes=uploaded_file.size,
            width=width,
            height=height
        )

        # Update profile storage stats
        if hasattr(request.user, 'profile'):
            request.user.profile.storage_used_bytes += uploaded_file.size
            request.user.profile.save(update_fields=['storage_used_bytes'])

        return Response(MediaAssetSerializer(asset, context={'request': request}).data, status=status.HTTP_201_CREATED)


class MediaAssetDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        asset = get_object_or_404(MediaAsset, id=pk, user=request.user)
        size = asset.size_bytes

        # Delete physical files
        if asset.file:
            asset.file.delete(save=False)
        if asset.thumbnail:
            asset.thumbnail.delete(save=False)
        asset.delete()

        # Update profile storage
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            profile.storage_used_bytes = max(0, profile.storage_used_bytes - size)
            profile.save(update_fields=['storage_used_bytes'])

        return Response({'message': 'Media asset deleted successfully.'})
