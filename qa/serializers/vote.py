# qa/serializers/vote.py
from rest_framework import serializers
from qa.models import Vote
from qa.serializers import QuestionSerializer, AnswerSerializer


class VoteSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    answer = AnswerSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ['id', 'vote_type', 'user', 'question', 'answer', 'created_at']
        read_only_fields = fields

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y年%m月%d日")