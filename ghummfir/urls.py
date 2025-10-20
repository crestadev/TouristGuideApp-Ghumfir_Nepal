from django.contrib import admin
from django.urls import path, include
from guides import views as guide_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', guide_views.home, name='home'),
    path('places/', include('guides.urls')),
]
