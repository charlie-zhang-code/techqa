# qa/models/answer.py
from django.db import models
from .base import BaseModel
from .user import User
from .question import Question

class Answer(BaseModel):
    content = models.TextField(verbose_name="内容")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='answers', verbose_name="作者"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers', verbose_name="问题"
    )
    votes = models.IntegerField(default=0, verbose_name="投票数")
    is_accepted = models.BooleanField(default=False, verbose_name="是否被采纳")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名回答")

    class Meta:
        verbose_name = "回答"
        verbose_name_plural = verbose_name
        ordering = ['-is_accepted', '-votes', '-created_at']

    def __str__(self):
        return f"{self.author.username}的回答"

    def update_votes(self):
        self.votes = self.answer_votes.filter(vote_type='up').count() - \
                     self.answer_votes.filter(vote_type='down').count()
        self.save()

    def accept(self):
        # 确保一个问题只有一个被采纳的回答
        Answer.objects.filter(question=self.question).update(is_accepted=False)
        self.is_accepted = True
        self.save()
        self.question.has_accepted_answer = True
        self.question.save()