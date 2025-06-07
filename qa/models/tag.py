# qa/models/tag.py
from django.db import models
from django.template.defaultfilters import slugify

from .base import BaseModel

class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    usage_count = models.PositiveIntegerField(default=0, verbose_name="使用次数")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)