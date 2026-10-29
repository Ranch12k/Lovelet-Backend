from django.db import models


class TemplateCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(max_length=50, default='Heart')
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Template Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Template(models.Model):
    category = models.ForeignKey(TemplateCategory, on_delete=models.CASCADE, related_name='templates')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    thumbnail_url = models.CharField(max_length=500, blank=True)
    envelope_theme = models.CharField(max_length=50, default='rose_gold')
    envelope_seal_text = models.CharField(max_length=50, default='LOVE')
    background_style = models.CharField(max_length=50, default='romantic_gradient')
    music_url = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    pages_data = models.JSONField(default=list)  # Pre-configured pages with rich content blocks
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'title']

    def __str__(self):
        return self.title
