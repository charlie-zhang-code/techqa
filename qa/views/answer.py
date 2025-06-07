# qa/views/answer.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from qa.models import Answer, Vote
from qa.serializers.answer import (
    AnswerSerializer, AnswerCreateSerializer,
    AnswerUpdateSerializer, AnswerAcceptSerializer,
    AnswerVoteSerializer
)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return AnswerCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AnswerUpdateSerializer
        elif self.action == 'accept':
            return AnswerAcceptSerializer
        elif self.action == 'vote':
            return AnswerVoteSerializer
        return AnswerSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        answer = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vote_type = serializer.validated_data['vote_type']
        vote, created = Vote.objects.update_or_create(
            user=request.user,
            answer=answer,
            defaults={'vote_type': vote_type}
        )

        answer.update_votes()
        return Response(AnswerSerializer(answer, context=self.get_serializer_context()).data)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        answer = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if answer.question.author != request.user:
            return Response({'error': '只有问题作者可以采纳回答'}, status=status.HTTP_403_FORBIDDEN)

        is_accepted = serializer.validated_data['is_accepted']
        if is_accepted:
            answer.accept()
        else:
            answer.is_accepted = False
            answer.save()
            answer.question.has_accepted_answer = False
            answer.question.save()

        return Response(AnswerSerializer(answer, context=self.get_serializer_context()).data)