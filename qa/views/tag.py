# qa/views/tag.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from qa.models import Tag
from qa.serializers.tag import TagSerializer, TagFollowSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'usage_count']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'follow':
            return TagFollowSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        tag = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        if action == 'follow':
            request.user.following_tags.add(tag)
        else:
            request.user.following_tags.remove(tag)

        return Response({'status': 'success'})

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular_tags = Tag.objects.order_by('-usage_count')[:10]
        serializer = self.get_serializer(popular_tags, many=True)
        return Response(serializer.data)