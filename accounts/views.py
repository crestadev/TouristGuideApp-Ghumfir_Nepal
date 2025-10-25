from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Favorite

from guides.models import Itinerary, Place



@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'All fields are required.')

    # Get user's itinerary
    itinerary = Itinerary.objects.filter(user=request.user).first()

    # Prepare coordinates for map (if any)
    places_with_coords = []
    if itinerary:
        for p in itinerary.places.all():
            if getattr(p, 'latitude', None) and getattr(p, 'longitude', None):
                places_with_coords.append({
                    'name': p.name,
                    'lat': float(p.latitude),
                    'lng': float(p.longitude),
                    'location': p.location,
                })

    # Get user's favorites (place IDs) for template
    user_favorites = request.user.favorites.values_list('place_id', flat=True)

    # Render template
    return render(request, 'accounts/profile.html', {
        'itinerary': itinerary,
        'places_with_coords': places_with_coords,
        'user_favorites': user_favorites,
    })

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def add_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.get_or_create(user=request.user, place=place)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def remove_favorite(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.filter(user=request.user, place=place).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def favorites_list(request):
    favorites = request.user.favorites.all()
    return render(request, 'accounts/favorites.html', {'favorites': favorites})
