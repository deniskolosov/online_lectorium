from rest_framework import filters as drf_filters, viewsets
from rest_framework_json_api import (django_filters, filters, relations,
                                     serializers)

from rest_framework.permissions import IsAuthenticated
from afi_backend.videocourses.models import VideoCourse

from afi_backend.videocourses.api.serializers import VideoCourseSerializer


class VideoCourseViewset(viewsets.ModelViewSet):
    queryset = VideoCourse.objects.all()
    serializer_class = VideoCourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_fields = {
        'lecturer__id': ('exact', ),
        'lecturer__name': ('exact', ),
        'category__name': ('icontains', ),
        'category__id': ('exact', ),
    }
    search_fields = ['name', 'description']
