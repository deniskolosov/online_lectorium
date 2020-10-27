


from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from afi_backend.blog.api.serializers import PostSerializer
from afi_backend.blog.models import Post


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
