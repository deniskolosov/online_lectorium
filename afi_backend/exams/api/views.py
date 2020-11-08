from rest_framework import (filters as drf_filters, permissions, status,
    viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_json_api import django_filters, filters

from afi_backend.exams.api.serializers import ExamSerializer, ExamProgressSerializer
from afi_backend.exams.models import Exam, Answer


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

    @action(detail=True,
            serializer_class=ExamProgressSerializer,
            url_path='progress',
            permission_classes=[IsAuthenticated])
    def progress(self, request, pk=None):
        # get progress for exam
        exam = self.get_object()
        serializer = self.serializer_class(exam.progress)

        return Response(serializer.data, status=status.HTTP_200_OK)


    @progress.mapping.put
    def update_progress(self, request, pk=None):
        # Update progress for exam
        exam = self.get_object()
        # Use answer_id from data and update progress with related Answer object
        answer_id = request.data["answer_id"]
        answer = Answer.objects.get(id=answer_id)
        exam.progress.chosen_answers.add(answer)
        exam.progress.save()

        serializer = self.serializer_class(exam.progress)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
