from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('favorites/toggle/<int:place_id>/', views.toggle_favorite, name='toggle_favorite'),
]
