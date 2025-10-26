from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),

    # Favorites / Wishlist URLs
    path('favorites/add/<int:place_id>/', views.add_favorite_ajax, name='add_favorite_ajax'),
    path('favorites/remove/<int:place_id>/', views.remove_favorite_ajax, name='remove_favorite_ajax'),
]
