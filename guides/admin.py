from django.contrib import admin
from .models import Category, Place, Hotel, Review, Itinerary

admin.site.register(Category)
admin.site.register(Place)
admin.site.register(Hotel)
admin.site.register(Review)
admin.site.register(Itinerary)
