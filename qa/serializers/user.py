# qa/serializers/user.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from qa.models import Tag

from rest_framework import serializers
from django.contrib.auth import get_user_model
from qa.models import Tag

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    following_users_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'avatar', 'bio', 'location', 'website',
            'reputation', 'date_joined', 'is_following', 'following_users_count',
            'followers_count', 'questions_count', 'answers_count'
        ]
        read_only_fields = fields

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following_users.filter(id=obj.id).exists()
        return False

    def get_following_users_count(self, obj):
        return obj.following_users.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_questions_count(self, obj):
        return obj.questions.count()

    def get_answers_count(self, obj):
        return obj.answers.count()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar', 'bio', 'location', 'website']
        extra_kwargs = {
            'username': {'required': True},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar', 'bio', 'location', 'website']


class UserFollowSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['follow', 'unfollow'])


class WxLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    encrypted_data = serializers.CharField(required=False)
    iv = serializers.CharField(required=False)