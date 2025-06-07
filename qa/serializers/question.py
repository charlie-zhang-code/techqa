# qa/serializers/question.py
from django.template.defaultfilters import slugify
from rest_framework import serializers
from qa.models import Question, Tag, Answer, Vote
from qa.serializers.tag import TagSerializer
from qa.serializers.answer import AnswerSerializer
from qa.serializers.user import UserSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    answers_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 'title', 'content', 'author', 'tags', 'views', 'votes',
            'created_at', 'updated_at', 'has_accepted_answer', 'is_anonymous',
            'answers', 'answers_count', 'comments_count', 'user_vote', 'is_following'
        ]
        read_only_fields = fields

    def get_answers_count(self, obj):
        return obj.answers.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = obj.question_votes.filter(user=request.user).first()
            if vote:
                return vote.vote_type
        return None

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following_users.filter(id=obj.author.id).exists()
        return False

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y年%m月%d日")


class QuestionCreateSerializer(serializers.ModelSerializer):
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'is_anonymous', 'tag_names']
        read_only_fields = []

    def create(self, validated_data):
        print(validated_data)
        tag_names = validated_data.pop('tag_names', [])
        question = Question.objects.create(**validated_data)
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            if not created:
                tag.slug = slugify(tag.name)
                counter = 1
                while Tag.objects.filter(slug=tag.slug).exclude(id=tag.id).exists():
                    tag.slug = f"{slugify(tag.name)}-{counter}"
                    counter += 1
                tag.save()
            tags.append(tag)
        question.tags.set(tags)
        return question


class QuestionUpdateSerializer(serializers.ModelSerializer):
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'is_anonymous', 'tag_names']

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', None)
        instance = super().update(instance, validated_data)

        if tag_names is not None:
            tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            instance.tags.set(tags)

        return instance


class QuestionVoteSerializer(serializers.Serializer):
    vote_type = serializers.ChoiceField(choices=Vote.VOTE_TYPES)
