from django.shortcuts import render
import random
from django.shortcuts import render
from scripts.get_image import search_images
from django.core.paginator import Paginator


# Create your views here.
def gallery_view(request):
    categories = [
        'nature',
        'technology',
        'business',
        'food',
        'animals',
        'sports',
        'landscape',
        'travel',
        'fashion',
    ]
    random_category = random.choice(categories)

    image_urls = search_images(
        'pixabay', random_category
    )  # або random.choice(['pixabay', 'pexels', 'unsplash', 'freepik'])
    background_url = image_urls[0] if isinstance(image_urls, list) else None

    context = {
        'title_of_app': 'Royalty-Free Search App',
        'background_url': background_url,
    }
    return render(request, 'gallery/gallery.html', context)
