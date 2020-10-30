from rest_framework_json_api import serializers
from afi_backend.blog.models import Post
from afi_backend.events.api.serializers import CategorySerializer
from afi_backend.users.api.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    included_serializers = {
        'category': CategorySerializer,
        'author': UserSerializer
    }

    class Meta:
        model = Post
        fields = [
            'created_at',
            'author',
            'content',
            'category',
            'picture',
            'name',
            'description',
        ]
