from djoser.email import ActivationEmail
from djoser.serializers import ActivationSerializer

from djoser import utils

from django.contrib.auth import get_user_model
from rest_framework import serializers

from afi_backend.events.api.serializers import (OfflineLectureSerializer,
                                                VideoLectureSerializer)
from afi_backend.payments.api.serializers import (
    UserMembershipSerializer, VideoLectureOrderItemSerializer)
from afi_backend.tickets.api.serializers import TicketSerializer
from django.conf import settings

from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    userpic = serializers.FileField(read_only=True)
    user_memberships = UserMembershipSerializer(read_only=True, many=True)

    included_serializers = {
        'offline_lectures': OfflineLectureSerializer,
        'user_memberships': UserMembershipSerializer
    }

    class Meta:
        model = User
        fields = [
            "email",
            "url",
            "password",
            "user_memberships",
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


class UserActivationSerializer(ActivationSerializer):
    uid = serializers.IntegerField()

    def validate(self, attrs):
        validated_data = {
            'uid': str(self.initial_data.get('uid')),
            'token': self.initial_data.get("token", "")
        }

        try:
            self.user = User.objects.get(
                pk=str(self.initial_data.get('uid', "")))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError({"uid": [self.error_messages[key_error]]},
                                  code=key_error)

        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("token", ""))
        if is_token_valid:
            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError({"token": [self.error_messages[key_error]]},
                                  code=key_error)
