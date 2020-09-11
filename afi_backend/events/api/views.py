from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework_json_api import relations, serializers, filters, django_filters
from rest_framework.filters import SearchFilter

from ..models import Event, OfflineLecture
from .serializers import EventSerializer, OfflineLectureSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.QueryParameterValidationFilter,
                       django_filters.DjangoFilterBackend,
                       )
    filterset_fields = {
        'event_type': ('exact',)
    }

class OfflineLectureViewset(viewsets.ModelViewSet):
    queryset = OfflineLecture.objects.all()
    serializer_class = OfflineLectureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.QueryParameterValidationFilter,
                       django_filters.DjangoFilterBackend,
                       )
    filterset_fields = {
        'lecture_date': ('exact',)
    }
