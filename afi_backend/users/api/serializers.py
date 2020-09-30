from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    userpic = serializers.FileField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "url",
            "password",
            "userpic",
            "name",
            "birthdate",
        ]

        extra_kwargs = {
            "url": {
                "view_name": "api:user-detail",
                "lookup_field": "email"
            },
            "password": {
                "write_only": True,
                "required": False,
            }
        }

    def create(self, validated_data):
        validated_data['username'] = validated_data.get('email')
        user = User.objects.create_user(**validated_data)
        return user


class UserpicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["userpic"]
