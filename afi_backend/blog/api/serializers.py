from rest_framework_json_api import serializers
from afi_backend.blog.models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['created_at', 'author', 'content'
                  ]
