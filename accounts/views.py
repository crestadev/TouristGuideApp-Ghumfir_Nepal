from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from guides.models import Itinerary




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
            if p.latitude and p.longitude:
                places_with_coords.append({
                    'name': p.name,
                    'lat': p.latitude,
                    'lng': p.longitude,
                    'location': p.location,
                })

    # Render template
    return render(request, 'accounts/profile.html', {
        'itinerary': itinerary,
        'places_with_coords': places_with_coords,
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
