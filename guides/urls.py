from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('places/', views.place_list, name='place_list'),
    path('places/<slug:slug>/', views.place_detail, name='place_detail'),
    path('places/add/<int:place_id>/', views.add_to_itinerary, name='add_to_itinerary'),
]
