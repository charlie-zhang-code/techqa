# qa/serializers/notification.py
from rest_framework import serializers
from qa.models import Notification
from qa.serializers.user import UserSerializer
from qa.serializers.question import QuestionSerializer
from qa.serializers.answer import AnswerSerializer
from qa.serializers.comment import CommentSerializer


class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'is_read', 'created_at',
            'actor', 'question', 'answer', 'comment'
        ]
        read_only_fields = fields
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y年%m月%d日")

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']