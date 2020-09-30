from django.contrib.auth import get_user_model
from rest_framework import status, parsers, response
from rest_framework.decorators import action, parser_classes
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import UserSerializer, UserpicSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "email"
    lookup_value_regex = "[^/]+"

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser, IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True,
            methods=["PUT"],
            serializer_class=UserpicSerializer,
            url_path='upload-userpic',
            url_name='upload_userpic',
            permission_classes=[IsAuthenticated])
    @parser_classes([parsers.MultiPartParser])
    def upload_userpic(self, request, username=None):
        obj = self.get_object()
        serializer = self.serializer_class(obj,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors,
                                 status.HTTP_400_BAD_REQUEST)
