from ..models import Ticket, Event, QRCode
from django.conf import settings

from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    activation_link = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = [
            'customer',
            'activation_link',
        ]

    def get_activation_link(self, obj):
        return f"{settings.SITE_URL}/api/tickets/activate/{obj.qrcode.code}"




class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'description',
        ]


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = [
            'scanned',
        ]
