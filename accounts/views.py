from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Favorite, Place
from django.http import JsonResponse

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
def add_favorite_ajax(request, place_id):
    place = Place.objects.get(id=place_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, place=place)
    if created:
        return JsonResponse({'status': 'added'})
    else:
        return JsonResponse({'status': 'exists'})

@login_required
def remove_favorite_ajax(request, place_id):
    try:
        favorite = Favorite.objects.get(user=request.user, place_id=place_id)
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    except Favorite.DoesNotExist:
        return JsonResponse({'status': 'not_found'})