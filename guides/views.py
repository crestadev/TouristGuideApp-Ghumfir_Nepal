from django.shortcuts import redirect, render, get_object_or_404
from .models import Place, Category, Itinerary, Favorite
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



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
    reviews = place.review_set.all()
    related_hotels = place.hotel_set.all()
    form = ReviewForm(request.POST or None)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, place=place).exists()

    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.place = place
        review.save()
        messages.success(request, "Review added successfully!")
        return redirect('place_detail', slug=slug)

    return render(request, 'places/detail.html', {
        'place': place,
        'reviews': reviews,
        'related_hotels': related_hotels,
        'form': form,
        'is_favorite': is_favorite,
    })

@login_required
def add_to_itinerary(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    itinerary, created = Itinerary.objects.get_or_create(user=request.user)
    itinerary.places.add(place)
    messages.success(request, f"{place.name} added to your itinerary!")
    return redirect('place_detail', slug=place.slug)



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


