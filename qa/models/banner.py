from django.db import models
from .base import BaseModel

class Banner(BaseModel):
    """
    轮播图模型
    """
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banners/', verbose_name="图片")
    url = models.URLField(blank=True, null=True, verbose_name="跳转链接")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    order = models.PositiveIntegerField(default=0, verbose_name="排序")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title