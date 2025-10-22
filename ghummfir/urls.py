from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from guides import views as guide_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', guide_views.home, name='home'),
    path('places/', include('guides.urls')),
    path('about/', guide_views.about, name='about'),
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('django.contrib.auth.urls')),  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)