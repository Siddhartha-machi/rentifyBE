from rest_framework import viewsets

from .models import *
from .serializers import *

class PropertyAPIVIEW(viewsets.ModelViewSet):
    serializer_class = PropertyListSerializer
    search_fields = ["place", "area"]
    ordering = ["price"]

    def get_queryset(self):
        queryset = Property.objects.all()
        b_rooms = self.request.query_params.get("bedrooms")
        baths = self.request.query_params.get("baths")
        price = self.request.query_params.get("price")

        if b_rooms:
            queryset = queryset.filter(bedrooms=b_rooms)
        if baths:
            queryset = queryset.filter(baths=baths)
        if price:
            queryset = queryset.filter(price=price)
        return queryset


class TagAPIVIEW(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CategoryAPIVIEW(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
