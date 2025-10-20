from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('<slug:slug>/', views.place_detail, name='place_detail'),
]
