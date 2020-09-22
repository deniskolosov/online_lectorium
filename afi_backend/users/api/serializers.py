from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "name", "url", "password"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
            "password": {"write_only": True, "required": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserpicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["userpic"]
