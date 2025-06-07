# qa/views/notification.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from qa.models import Notification
from qa.serializers.notification import NotificationSerializer, NotificationUpdateSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    # 添加 queryset 属性
    queryset = Notification.objects.all()

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'count': count})

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'marked_read': updated})