# qa/models/vote.py
from django.db import models
from rest_framework.exceptions import ValidationError

from .base import BaseModel
from .user import User
from .question import Question
from .answer import Answer


class Vote(BaseModel):
    VOTE_TYPES = (
        ('up', '赞同'),
        ('down', '反对'),
    )

    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES, verbose_name="投票类型")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='votes', verbose_name="用户"
    )

    # 投票可以针对问题或回答
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='question_votes', null=True, blank=True, verbose_name="问题"
    )
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='answer_votes', null=True, blank=True, verbose_name="回答"
    )

    class Meta:
        verbose_name = "投票"
        verbose_name_plural = verbose_name
        unique_together = [
            ['user', 'question'],
            ['user', 'answer'],
        ]

    def __str__(self):
        return f"{self.user.username}的投票"

    def clean(self):
        if not self.question and not self.answer:
            raise ValidationError("投票必须关联问题或回答")
        if self.question and self.answer:
            raise ValidationError("投票不能同时关联问题和回答")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.question:
            self.question.update_votes()
        elif self.answer:
            self.answer.update_votes()