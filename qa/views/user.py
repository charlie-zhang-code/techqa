# qa/views/user.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from qa.serializers.user import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    UserFollowSerializer, WxLoginSerializer
)
from qa.services.wx_auth import WxAuthService
from qa.services.jwt import get_tokens_for_user

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'wx_login']:
            return []
        elif self.action in ['update', 'partial_update', 'destroy', 'follow']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'follow':
            return UserFollowSerializer
        elif self.action == 'wx_login':
            return WxLoginSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        if action == 'follow':
            request.user.following_users.add(user)
        else:
            request.user.following_users.remove(user)

        return Response({'status': 'success'})

    @action(detail=False, methods=['post'])
    def wx_login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        wx_auth = WxAuthService()
        wx_user_info = wx_auth.get_wx_user_info(code)

        if not wx_user_info:
            return Response({'error': '微信登录失败'}, status=status.HTTP_400_BAD_REQUEST)

        openid = wx_user_info.get('openid')
        user, created = User.objects.get_or_create(wx_openid=openid)

        if created:
            # 新用户，设置默认用户名
            user.username = f'wxuser_{user.id}'
            user.save()

        tokens = get_tokens_for_user(user)
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'tokens': tokens
        })