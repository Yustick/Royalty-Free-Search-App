from django.shortcuts import render

from scripts.get_image import category_thumbnails_array, search_images

SERVICE_API_NAME = 'pixabay'


def home_view(request):
    image_urls = search_images(SERVICE_API_NAME)
    background_url = image_urls[0] if isinstance(image_urls, list) else None

    context = {
        'background_url': background_url,
    }
    return render(request, 'core/home.html', context)


def categories_view(request):
    context = {
        'categories': category_thumbnails_array(),
    }

    return render(request, 'core/categories.html', context)


def about_view(request):
    image_urls = search_images(SERVICE_API_NAME)
    background_url = image_urls[0] if isinstance(image_urls, list) else None

    context = {
        'background_url': background_url,
    }
    return render(request, 'core/about.html', context)
