# qa/models/user.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from .base import BaseModel


class User(AbstractUser, BaseModel):
    wx_openid = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name="微信OpenID")
    wx_unionid = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name="微信UnionID")
    avatar = models.URLField(max_length=255, blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, null=True, verbose_name="个人简介")
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name="所在地")
    website = models.URLField(blank=True, null=True, verbose_name="个人网站")
    reputation = models.IntegerField(default=0, verbose_name="声望")

    # 关注相关
    following_users = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers', blank=True, verbose_name="关注的用户"
    )
    following_tags = models.ManyToManyField(
        'Tag', related_name='followers', blank=True, verbose_name="关注的标签"
    )

    # 添加自定义的 related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="qa_user_set",
        related_query_name="qa_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="qa_user_set",
        related_query_name="qa_user",
    )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username