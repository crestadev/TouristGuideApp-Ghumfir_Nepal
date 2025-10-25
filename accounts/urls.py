from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),

    # Favorites / Wishlist URLs
    path('favorites/add/<int:place_id>/', views.add_favorite, name='add_favorite'),
    path('favorites/remove/<int:place_id>/', views.remove_favorite, name='remove_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),  # optional page to list all favorites
]
