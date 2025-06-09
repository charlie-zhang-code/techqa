# qa/views/question.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from qa.models import Question, Vote, Comment
from qa.serializers import AnswerSerializer, CommentSerializer
from qa.serializers.question import (
    QuestionSerializer, QuestionCreateSerializer,
    QuestionUpdateSerializer, QuestionVoteSerializer
)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().prefetch_related('answers')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['author', 'tags', 'has_accepted_answer']
    filterset_fields = {
        'author': ['exact'],
        'tags__name': ['exact'],  # 修改这里，按标签名称过滤
        'has_accepted_answer': ['exact']
    }
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'views', 'votes']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return QuestionUpdateSerializer
        elif self.action == 'vote':
            return QuestionVoteSerializer
        return QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        question = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vote_type = serializer.validated_data['vote_type']
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            question=question,
            defaults={'vote_type': vote_type}
        )

        question.update_votes()
        return Response(QuestionSerializer(question, context=self.get_serializer_context()).data)

    @action(detail=True, methods=['post'], url_path='increment_views')
    def increment_views(self, request, pk=None):
        question = self.get_object()
        question.views += 1
        question.save()
        return Response({'status': 'success'})

    @action(detail=True, methods=['get'], url_path='answers')
    def get_answers(self, request, pk=None):
        """获取特定问题的所有回答"""
        question = self.get_object()
        answers = question.answers.all()
        serializer = AnswerSerializer(answers, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='comments')
    def get_comments(self, request, pk=None):
        """获取特定问题的所有评论"""
        question = self.get_object()
        comments = Comment.objects.filter(question=question)
        serializer = CommentSerializer(comments, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def hot(self, request):
        """获取热门问题列表"""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('-hot_score')[:10]  # 取前20个热门问题
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)