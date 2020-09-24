from rest_framework import filters as drf_filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import django_filters, filters, relations, serializers

from ..models import Event, Category, Lecturer, OfflineLecture, VideoLecture
from .serializers import (
    EventSerializer,
    CategorySerializer,
    LecturerSerializer,
    OfflineLectureSerializer,
    VideoLectureSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend, )
    filterset_fields = {'event_type': ('exact', )}


class OfflineLectureViewset(viewsets.ModelViewSet):
    queryset = OfflineLecture.objects.all()
    serializer_class = OfflineLectureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_fields = {
        'lecture_date': (
            'exact',
            'week_day',
            'gt',
            'lt',
        ),
        'lecturer__id': ('exact', ),
        'lecturer__name': ('exact', ),
        'category__name': ('icontains', ),
        'category__id': ('exact', ),
    }
    search_fields = ['name']


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    permission_classes = [IsAuthenticated]
    filterset_fields = {'name': ('icontains', )}
    search_fields = ['name']


class LecturersViewset(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_fields = {'name': ('icontains', )}
    search_fields = ['name']


class VideoLectureViewset(viewsets.ModelViewSet):
    queryset = VideoLecture.objects.all()
    serializer_class = VideoLectureSerializer
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
