from django.shortcuts import render
from scripts.get_image import (
    search_images,
    random_category,
    category_thumbnails_array,
    fetch_images,
)
from django.core.paginator import Paginator


# Create your views here.
def gallery_view(request):

    context = {
        'title_of_app': 'Royalty-Free Search App',
    }
    return render(request, 'gallery/gallery.html', context)
