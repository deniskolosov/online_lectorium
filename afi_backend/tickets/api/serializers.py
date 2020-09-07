from ..models import Ticket, Event, QRCode

from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'customer',
            'event_type',
        ]


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
