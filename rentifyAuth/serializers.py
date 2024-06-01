from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from rest_framework import serializers

from .models import *


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("groups", "user_permissions")

    def create(self, attrs):
        user = User.objects.create_user(**attrs)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "groups", "user_permissions")
