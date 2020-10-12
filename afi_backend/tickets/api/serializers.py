from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from rest_framework_json_api import serializers

from afi_backend.events.api.serializers import EventTypeSerializer
from afi_backend.tickets.models import QRCode, Ticket
from afi_backend.events.api.serializers import OfflineLectureSerializer
from afi_backend.users.models import User
from afi_backend.events.models import OfflineLecture


class TicketSerializer(serializers.ModelSerializer):
    activation_link = serializers.SerializerMethodField()
    scanned = serializers.BooleanField(read_only=True)
    included_serializers = {
        'offline_lecture': OfflineLectureSerializer,
    }
    customer_email = serializers.EmailField(source='customer.email')
    offline_lecture_id = serializers.IntegerField(source='offline_lecture.id')
    offline_lecture = serializers.ResourceRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'customer_email',
            'activation_link',
            'offline_lecture',
            'scanned',
            'offline_lecture_id',
        ]

    def get_activation_link(self, obj):
        if obj.get_qr_code():
            return f"{settings.SITE_URL}/api/tickets/activate/{obj.qrcode.code}"
        return ""

    def create(self, validated_data):
        customer = validated_data.get('customer')
        offline_lecture = validated_data.get('offline_lecture')
        customer = User.objects.get(email=customer.get('email'))
        offline_lecture = OfflineLecture.objects.get(
            id=offline_lecture.get('id'))
        return Ticket.objects.create(customer=customer,
                                     offline_lecture=offline_lecture)


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = [
            'scanned',
        ]
