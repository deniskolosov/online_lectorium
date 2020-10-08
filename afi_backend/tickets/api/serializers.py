from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework_json_api import serializers

from afi_backend.events.api.serializers import EventTypeSerializer
from afi_backend.tickets.models import QRCode, Ticket
from afi_backend.events.api.serializers import OfflineLectureSerializer


class TicketSerializer(serializers.ModelSerializer):
    activation_link = serializers.SerializerMethodField()
    scanned = serializers.BooleanField(read_only=True)
    included_serializers = {
        'offline_lecture': OfflineLectureSerializer,
    }

    class Meta:
        model = Ticket
        fields = [
            'customer',
            'activation_link',
            'scanned',
            'offline_lecture',
        ]

    def get_activation_link(self, obj):
        if obj.get_qr_code():
            return f"{settings.SITE_URL}/api/tickets/activate/{obj.qrcode.code}"
        return ""


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = [
            'scanned',
        ]
