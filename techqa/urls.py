# techqa/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from qa.views import (
    UserViewSet, TagViewSet, QuestionViewSet,BannerViewSet,
    AnswerViewSet, CommentViewSet, NotificationViewSet, VoteViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tags', TagViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'banners', BannerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # OpenAPI生成端点
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI:
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Redoc UI:
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)