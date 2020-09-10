from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from ..models import QRCode, Ticket
from .serializers import QRCodeSerializer, TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing tickets.
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[], url_path='activate/(?P<qr_code>[^/.]+)')
    def activate(self, request, qr_code, pk=None):
        try:
            qr_code_object = QRCode.objects.get(code=qr_code)
        except QRCode.DoesNotExist:
            return Response({"error": "No such code"}, status=status.HTTP_404_NOT_FOUND)

        if qr_code_object.is_valid():
            qr_code_object.activate()
            return Response({"msg": "Activated"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Code"}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        tickets = Ticket.objects.filter(customer=user)
        return tickets


class QRCodeViewSet(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = [IsAdminUser]
