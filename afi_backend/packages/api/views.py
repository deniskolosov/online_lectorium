from rest_framework import filters as drf_filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_json_api import django_filters, filters, relations, serializers
from afi_backend.packages.models import VideoLecturePackage, VideoCoursePackage
from afi_backend.packages.api.serializers import VideoLecturePackageSerializer, VideoCoursePackageSerializer


class VideoLecturePackageViewset(viewsets.ModelViewSet):
    queryset = VideoLecturePackage.objects.all()
    serializer_class = VideoLecturePackageSerializer
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    permission_classes = [IsAuthenticatedOrReadOnly]


class VideoCoursePackageViewset(viewsets.ModelViewSet):
    queryset = VideoCoursePackage.objects.all()
    serializer_class = VideoCoursePackageSerializer
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
