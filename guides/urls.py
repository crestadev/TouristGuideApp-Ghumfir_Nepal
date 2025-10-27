from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('<slug:slug>/', views.place_detail, name='place_detail'),
    path('add/<int:place_id>/', views.add_to_itinerary, name='add_to_itinerary'),
    path('places/favorite/<int:place_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('places/unfavorite/<int:place_id>/', views.remove_from_favorites, name='remove_from_favorites'),

]
