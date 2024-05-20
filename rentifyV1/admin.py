from django.contrib import admin

from .models import *

# registering the models to the admin site
admin.site.register(Property)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Category)
