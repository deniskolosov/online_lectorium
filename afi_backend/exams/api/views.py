from afi_backend.exams.models import Exam
from afi_backend.exams.api.serializers import ExamSerializer
from rest_framework import permissions
from rest_framework_json_api import django_filters, filters

from rest_framework import filters as drf_filters, viewsets


class ExamViewset(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (
        filters.QueryParameterValidationFilter,
        django_filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_fields = {
    }
    search_fields = []
