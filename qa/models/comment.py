# qa/models/comment.py
from django.db import models
from rest_framework.exceptions import ValidationError

from .base import BaseModel
from .user import User
from .question import Question
from .answer import Answer


class Comment(BaseModel):
    content = models.TextField(verbose_name="内容")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name="作者"
    )

    # 评论可以针对问题或回答
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='comments', null=True, blank=True, verbose_name="问题"
    )
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='comments', null=True, blank=True, verbose_name="回答"
    )

    reply_to = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="回复"
    )

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username}的评论"

    def clean(self):
        if not self.question and not self.answer:
            raise ValidationError("评论必须关联问题或回答")
        if self.question and self.answer:
            raise ValidationError("评论不能同时关联问题和回答")