# qa/models/notification.py
from django.db import models
from .base import BaseModel
from .user import User
from .question import Question
from .answer import Answer
from .comment import Comment


class Notification(BaseModel):
    NOTIFICATION_TYPES = (
        ('question_answered', '问题被回答'),
        ('answer_commented', '回答被评论'),
        ('answer_accepted', '回答被采纳'),
        ('mentioned', '被提及'),
    )

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name="通知类型")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications', verbose_name="接收者"
    )
    is_read = models.BooleanField(default=False, verbose_name="是否已读")

    # 通知关联的内容
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True, verbose_name="问题"
    )
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="回答"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True, verbose_name="评论"
    )

    # 触发通知的用户
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='acted_notifications', verbose_name="触发者"
    )

    class Meta:
        verbose_name = "通知"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()}通知"