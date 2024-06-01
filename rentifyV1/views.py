from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import *
from .serializers import *


class PropertyAPIVIEW(viewsets.ModelViewSet):
    serializer_class = PropertyListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["place", "street", "property_name"]
    ordering = ["price", "bedrooms", "baths"]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Property.objects.all()
        seller = self.request.query_params.get("byseller")
        b_rooms = self.request.query_params.get("bedrooms")
        baths = self.request.query_params.get("baths")
        price = self.request.query_params.get("price")
        location = self.request.query_params.get("location")
        amenities = self.request.query_params.get('amenities')
        categories = self.request.query_params.get("categories")

        if location:
            queryset = queryset.filter(location=location)
        if amenities:
            lst = amenities.split(',')
            queryset = queryset.filter(amenities__in=lst).distinct()
        if categories:
            lst = categories.split(",")
            queryset = queryset.filter(category__in=lst).distinct()
        if b_rooms:
            queryset = queryset.filter(bedrooms=b_rooms)
        if baths:
            queryset = queryset.filter(baths=baths)
        if price:
            price = price.split(",")
            lp, hp = int(price[0]), int(price[-1])
            queryset = queryset.filter(price__gte=lp, price__lte=hp)
        if seller:
            queryset = queryset.filter(seller=seller)
        return queryset


class TagAPIVIEW(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class CategoryAPIVIEW(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class LocationAPIVIEW(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = None
