from django.shortcuts import redirect, render, get_object_or_404
from .models import Place, Category, Itinerary
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
    related_hotels = place.hotels.all()
    reviews = place.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            review.save()
            return redirect('place_detail', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'places/detail.html', {
        'place': place,
        'related_hotels': related_hotels,
        'reviews': reviews,
        'form': form,
    })

@login_required
def add_to_itinerary(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    itinerary, created = Itinerary.objects.get_or_create(user=request.user)
    itinerary.places.add(place)
    messages.success(request, f"{place.name} added to your itinerary!")
    return redirect('place_detail', slug=place.slug)