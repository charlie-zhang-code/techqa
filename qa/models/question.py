# qa/models/question.py
from django.db import models
from .base import BaseModel
from .user import User
from .tag import Tag

class Question(BaseModel):
    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='questions', verbose_name="作者"
    )
    tags = models.ManyToManyField(Tag, related_name='questions', verbose_name="标签")
    views = models.PositiveIntegerField(default=0, verbose_name="浏览数")
    votes = models.IntegerField(default=0, verbose_name="投票数")
    has_accepted_answer = models.BooleanField(default=False, verbose_name="有采纳的回答")
    is_anonymous = models.BooleanField(default=False, verbose_name="匿名提问")
    hot_score = models.FloatField(default=0, verbose_name="热门分数")

    class Meta:
        verbose_name = "问题"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def update_votes(self):
        self.votes = self.question_votes.filter(vote_type='up').count() - \
                     self.question_votes.filter(vote_type='down').count()
        self.save()

    def update_hot_score(self):
        """更新问题的热门分数"""
        # 使用类似Reddit的热门算法：分数 = (回答数*5 + 投票数*2 + 浏览数*0.1) / (小时差+2)^1.5
        from django.utils.timezone import now
        hours_passed = (now() - self.created_at).total_seconds() / 3600
        self.hot_score = (self.answers.count() * 5 + self.votes * 2 + self.views * 0.1) / pow(hours_passed + 2, 1.5)
        self.save()