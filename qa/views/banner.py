from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from qa.models import Banner
from qa.serializers.banner import BannerSerializer

class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # 禁用分页