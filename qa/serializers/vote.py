# qa/serializers/vote.py
from rest_framework import serializers
from qa.models import Vote

class VoteSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ['id', 'vote_type', 'user', 'question', 'answer', 'created_at']
        read_only_fields = fields

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y年%m月%d日")