from django.urls import path, include

from rest_framework import routers

from rentifyAuth.views import *


urlpatterns = [
    path("", UserListAPI.as_view()),
    path("auth-register/", UserRegisterAPI.as_view()),
    path("<str:email>/", UserRetrieveAPI.as_view()),
]
