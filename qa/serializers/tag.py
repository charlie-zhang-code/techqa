# qa/serializers/tag.py
from rest_framework import serializers
from qa.models import Tag


class TagSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description', 'usage_count', 'is_following']
        read_only_fields = fields

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following_tags.filter(id=obj.id).exists()
        return False


class TagFollowSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['follow', 'unfollow'])