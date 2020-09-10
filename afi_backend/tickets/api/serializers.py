from afi_backend.users.api.serializers import UserSerializer
from ..models import Ticket, QRCode
from django.conf import settings
from afi_backend.events.api.serializers import EventTypeSerializer

from rest_framework_json_api import serializers


class TicketSerializer(serializers.ModelSerializer):
    activation_link = serializers.SerializerMethodField()
    scanned = serializers.BooleanField()
    event_type = EventTypeSerializer(source='content_object', read_only=True)
    class Meta:
        model = Ticket
        fields = [
            'customer',
            'activation_link',
            'scanned',
            'event_type',
        ]


    def get_activation_link(self, obj):
        if hasattr(obj, 'qrcode'):
            return f"{settings.SITE_URL}/api/tickets/activate/{obj.qrcode.code}"
        else:
            return ""

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = [
            'scanned',
        ]
