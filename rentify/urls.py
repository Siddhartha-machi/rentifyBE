"""
URL configuration for rentify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework.authtoken import views

from . import settings

BASE_END = settings.BASE_URL + "v" + settings.APP_VERSION

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{BASE_END}/auth-token/", views.obtain_auth_token),
    path(f"{BASE_END}/users/", include("rentifyAuth.urls")),
    path(f"{BASE_END}/", include("rentifyV1.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
