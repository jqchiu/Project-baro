from django.contrib import admin
from .models import Listing, Photo, Review, Profile


admin.site.register(Listing)
admin.site.register(Photo)
admin.site.register(Review)
admin.site.register(Profile)