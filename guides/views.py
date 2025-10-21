from django.shortcuts import redirect, render, get_object_or_404
from .models import Place, Category
from .forms import ReviewForm


def home(request):
    return render(request, 'home.html')



def place_list(request):
    categories = Category.objects.all()
    places = Place.objects.all().order_by('name')
    return render(request, 'places/list.html', {'places': places, 'categories': categories})

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
