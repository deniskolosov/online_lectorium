from ..models import Ticket, Event, QRCode
from .serializers import TicketSerializer, EventSerializer, QRCodeSerializer
from rest_framework import viewsets

class TicketViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing tickets.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = []


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = []



class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = []
