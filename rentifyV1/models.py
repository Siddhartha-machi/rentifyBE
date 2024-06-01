from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rentify.settings import AUTH_USER_MODEL


class Image(models.Model):
    image = models.ImageField(verbose_name="Property image", upload_to="property_pics")

    def __str__(self):
        return "Image" + str(self.id)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Tag name")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Category name")

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Location name")

    def __str__(self):
        return self.name


class Property(models.Model):
    """
    Defines the property model definition
    with all the essential attributes.
    """

    property_name = models.CharField(
        max_length=100, verbose_name="Property name", unique=True
    )
    price = models.BigIntegerField(verbose_name="Price of the property")
    location = models.ForeignKey(to=Location, on_delete=models.CASCADE)
    place = models.CharField(max_length=250, verbose_name="Where property is located")
    street = models.CharField(
        max_length=150, verbose_name="Street in which proerty located"
    )
    bedrooms = models.PositiveIntegerField(
        verbose_name="No of bed rooms in the property"
    )
    baths = models.PositiveIntegerField(verbose_name="No of baths in the property")

    seller = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    like = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name="likes")
    wishlist = models.ManyToManyField(
        AUTH_USER_MODEL, blank=True, related_name="whishlist"
    )
    images = models.OneToOneField(
        to=Image, null=True, blank=True, on_delete=models.CASCADE
    )
    amenities = models.ManyToManyField(to=Tag, blank=True)
    category = models.ManyToManyField(to=Category, blank=True)

    def __str__(self):
        return self.property_name

    def clean(self):
        if self.seller.role != "seller":
            raise ValidationError(
                {
                    "seller": _(
                        "Invalid role assigned to the field. Only user with seller role can be assigned to the field."
                    )
                }
            )
