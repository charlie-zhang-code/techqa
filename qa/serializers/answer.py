# qa/serializers/answer.py
from rest_framework import serializers
from qa.models import Answer, Vote
from qa.serializers.user import UserSerializer
from qa.serializers.comment import CommentSerializer


class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = [
            'id', 'content', 'author', 'question', 'votes', 'is_accepted',
            'is_anonymous', 'created_at', 'updated_at', 'comments',
            'comments_count', 'user_vote'
        ]
        read_only_fields = fields

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = obj.answer_votes.filter(user=request.user).first()
            if vote:
                return vote.vote_type
        return None
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y年%m月%d日")


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content', 'question', 'is_anonymous']
        extra_kwargs = {
            'question': {'required': True},
        }


class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content', 'is_anonymous']


class AnswerAcceptSerializer(serializers.Serializer):
    is_accepted = serializers.BooleanField()


class AnswerVoteSerializer(serializers.Serializer):
    vote_type = serializers.ChoiceField(choices=Vote.VOTE_TYPES)