from rest_framework import serializers

from rentifyV1.models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PropertyListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    images = ImageSerializer()

    class Meta:
        model = Property
        fields = "__all__"
