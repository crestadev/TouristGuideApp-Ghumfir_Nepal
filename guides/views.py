from datetime import date
from django.shortcuts import redirect, render, get_object_or_404
from .models import Favorite, ItineraryItem, Place, Category, Itinerary, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .utils import get_weather



def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')



def place_list(request):
    categories = Category.objects.all()
    places = Place.objects.all().order_by('name')

    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    if search_query:
        places = places.filter(name__icontains=search_query) | places.filter(location__icontains=search_query)

    if category_filter:
        places = places.filter(category__id=category_filter)

    context = {
        'places': places,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'places/list.html', context)

def place_detail(request, slug):
    place = get_object_or_404(Place, slug=slug)
    weather = get_weather(place.latitude, place.longitude)

    related_hotels = getattr(place, 'hotels', []).all()  # if hotels exist
    reviews = place.reviews.all().order_by('-created_at')
    average_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    if request.user.is_authenticated and request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save or update review for this user & place
            review, created = Review.objects.update_or_create(
                user=request.user,
                place=place,
                defaults=form.cleaned_data
            )
            messages.success(request, "Your review has been submitted!")
            return redirect('place_detail', slug=slug)
    else:
        # Pre-fill form if user already reviewed
        if request.user.is_authenticated:
            try:
                existing = Review.objects.get(user=request.user, place=place)
                form = ReviewForm(instance=existing)
            except Review.DoesNotExist:
                form = ReviewForm()
        else:
            form = None  # non-logged-in users can't submit

    return render(request, 'places/detail.html', {
        'place': place,
        'related_hotels': related_hotels,
        'reviews': reviews,
        'average_rating': average_rating,
        'form': form,
        'weather': weather,

    })

@login_required
def add_to_itinerary(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    itinerary, created = Itinerary.objects.get_or_create(user=request.user)

    if not ItineraryItem.objects.filter(itinerary=itinerary, place=place).exists():
        ItineraryItem.objects.create(
            itinerary=itinerary,
            place=place,
            start_date=date.today(),
            end_date=date.today()
        )
        messages.success(request, f"{place.name} added to your itinerary!")
    else:
        messages.info(request, f"{place.name} is already in your itinerary.")

    return redirect('place_detail', slug=place.slug)

@login_required
def remove_from_itinerary(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    itinerary = Itinerary.objects.filter(user=request.user).first()
    if itinerary and place in itinerary.places.all():
        itinerary.places.remove(place)
    return redirect('profile')


@login_required
def add_to_favorites(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, place=place)
    if created:
        messages.success(request, f"{place.name} added to your favorites!")
    else:
        messages.info(request, f"{place.name} is already in your favorites.")
    return redirect('place_detail', slug=place.slug)


@login_required
def remove_from_favorites(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    Favorite.objects.filter(user=request.user, place=place).delete()
    messages.success(request, f"{place.name} removed from your favorites.")
    return redirect('profile')
