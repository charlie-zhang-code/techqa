# qa/admin.py
from django.contrib import admin
from qa.models import User, Question, Answer, Comment, Vote, Tag, Notification, Banner

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'date_joined')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'views', 'votes', 'has_accepted_answer')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'tags')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'question', 'created_at', 'votes', 'is_accepted')
    search_fields = ('content',)
    list_filter = ('created_at', 'is_accepted')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'question', 'answer', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'usage_count')
    search_fields = ('name',)
    list_filter = ('usage_count',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_type', 'recipient', 'actor', 'created_at')
    list_filter = ('notification_type', 'created_at')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'url', 'is_active', 'order')
    list_filter = ('is_active', 'order')

# 注册自定义的Admin类
admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Banner, BannerAdmin)