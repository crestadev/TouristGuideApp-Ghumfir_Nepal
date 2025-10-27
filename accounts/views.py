from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from guides.models import  Itinerary

# Profile view
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

    # Prepare coordinates for map
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

    # User's favorite place IDs
    user_favorites = request.user.favorites.values_list('place_id', flat=True)

    return render(request, 'accounts/profile.html', {
        'itinerary': itinerary,
        'places_with_coords': places_with_coords,
        'user_favorites': user_favorites,
    })

# Signup view
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
