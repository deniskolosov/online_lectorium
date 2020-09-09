from afi_backend.users.api.serializers import UserSerializer
from ..models import Ticket, QRCode
from django.conf import settings

from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    activation_link = serializers.SerializerMethodField()
    scanned = serializers.BooleanField()
    customer = UserSerializer()
    class Meta:
        model = Ticket
        fields = [
            'customer',
            'activation_link',
            'scanned',
        ]


    def get_activation_link(self, obj):
        if hasattr(obj, 'qrcode'):
            return f"{settings.SITE_URL}/api/tickets/activate/{obj.qrcode.code}"
        else:
            return ""



# TODO: move to events app
# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = [
#             'name',
#             'category',
#             'description',
#         ]
#         filterset_fields = ['category']
#         search_fields = ['name']


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = [
            'scanned',
        ]
