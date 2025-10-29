from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from guides.models import Itinerary, ItineraryItem, Favorite
from guides.forms import ItineraryItemForm


#  Signup view (User Registration)
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to Ghumfir Nepal 🇳🇵")
            return redirect('/')
        else:
            messages.error(request, "Something went wrong. Please check your details.")
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})



@login_required
def profile_view(request):
    user = request.user

    # -----------------------------
    # Handle profile updates
    # -----------------------------
    if request.method == 'POST' and 'update_profile' in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'All fields are required.')

    # -----------------------------
    # Fetch user's itinerary items
    # -----------------------------
    itinerary = Itinerary.objects.filter(user=user).first()
    itinerary_items = ItineraryItem.objects.filter(itinerary=itinerary).select_related('place') if itinerary else []

    # Handle date updates for itinerary items
    if request.method == 'POST' and 'update_dates' in request.POST:
        item_id = request.POST.get('item_id')
        item = ItineraryItem.objects.get(id=item_id)
        form = ItineraryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated dates for {item.place.name}.")
            return redirect('profile')
        else:
            messages.error(request, f"Invalid dates for {item.place.name}.")

    # Create forms for each itinerary item to render in template
    itinerary_forms = [(item, ItineraryItemForm(instance=item)) for item in itinerary_items]

    # -----------------------------
    # Collect map coordinates
    # -----------------------------
    places_with_coords = []
    for item in itinerary_items:
        place = item.place
        if getattr(place, 'latitude', None) and getattr(place, 'longitude', None):
            places_with_coords.append({
                'name': place.name,
                'lat': float(place.latitude),
                'lng': float(place.longitude),
                'location': place.location,
            })

    # -----------------------------
    # Fetch user's favorites
    # -----------------------------
    favorites = Favorite.objects.filter(user=user).select_related('place')
    user_favorites = favorites.values_list('place_id', flat=True)

    # -----------------------------
    # Render profile template
    # -----------------------------
    return render(request, 'accounts/profile.html', {
        'itinerary': itinerary,
        'itinerary_items': itinerary_items,
        'itinerary_forms': itinerary_forms,  
        'places_with_coords': places_with_coords,
        'favorites': favorites,
        'user_favorites': user_favorites,
    })

