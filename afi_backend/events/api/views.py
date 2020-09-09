from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from ..models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['category']
