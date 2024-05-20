from django.urls import path, include

from rest_framework import routers

from rentifyV1.views import *


router = routers.DefaultRouter()
router.register("property-list", PropertyAPIVIEW, basename=Property)
router.register("tags-list", TagAPIVIEW, basename=Tag)
router.register("category-list", CategoryAPIVIEW, basename=Category)

urlpatterns = [
    path("", include(router.urls)),
]
