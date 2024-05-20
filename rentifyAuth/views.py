from django.http import Http404

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework import parsers, renderers
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import *
from .models import *

# Rentify user API views


class UserRegisterAPI(CreateAPIView):
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RegisterUserSerializer
    permission_classes = []


class UserListAPI(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get("role")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if role:
            queryset = queryset.filter(role=role)
        if first_name:
            queryset = queryset.filter(first_name=first_name)
        if last_name:
            queryset = queryset.filter(last_name=last_name)
        return queryset


class UserRetrieveAPI(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"
    permission_classes = [IsAuthenticated]
