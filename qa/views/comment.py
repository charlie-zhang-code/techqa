# qa/views/comment.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from qa.models import Comment
from qa.serializers.comment import CommentSerializer, CommentCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)