from django.contrib.auth import get_user_model
from rest_framework import serializers
from afi_backend.payments.api.serializers import VideoLectureOrderItemSerializer
from afi_backend.tickets.api.serializers import TicketSerializer
from afi_backend.events.api.serializers import VideoLectureSerializer
from afi_backend.tickets.api.serializers import TicketSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    userpic = serializers.FileField(read_only=True)
    purchased_items = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "url",
            "password",
            "userpic",
            "name",
            "birthdate",
            "purchased_items",
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

    def get_purchased_items(self, obj):
        data = {
            "video_lectures":
            VideoLectureOrderItemSerializer(
                obj.videolectureorderitem_set.all(), many=True).data,
            "tickets":
            TicketSerializer(obj.ticket_set.all(), many=True).data
        }
        return data


class UserpicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["userpic"]


class UserPurchasedItemsSerializer(serializers.ModelSerializer):
    video_lectures = VideoLectureSerializer(many=True)
    tickets = TicketSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'video_lectures',
            'tickets',
        ]
