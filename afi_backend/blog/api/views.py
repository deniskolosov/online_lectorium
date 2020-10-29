
from rest_framework import filters as drf_filters
from rest_framework_json_api import django_filters, filters


from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from afi_backend.blog.api.serializers import PostSerializer
from afi_backend.blog.models import Post


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    queryset = Post.objects.all()

    filter_backends = (
        django_filters.DjangoFilterBackend,
    )
    filterset_fields = {
        'category__id': ('exact', ),
    }
