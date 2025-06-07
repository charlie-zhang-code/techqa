# qa/serializers/comment.py
from rest_framework import serializers
from qa.models import Comment
from qa.serializers.user import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    reply_to = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'question', 'answer', 'reply_to', 'created_at', 'replies']
        read_only_fields = fields

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True, context=self.context).data
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y年%m月%d日")

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'question', 'answer', 'reply_to']

    def validate(self, data):
        if not data.get('question') and not data.get('answer'):
            raise serializers.ValidationError("评论必须关联问题或回答")
        if data.get('question') and data.get('answer'):
            raise serializers.ValidationError("评论不能同时关联问题和回答")
        return data