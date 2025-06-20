from django.shortcuts import render

from scripts.get_image import category_thumbnails_array, search_images

SERVICE_API_NAME = 'pixabay'


def home_view(request):
    images = search_images(SERVICE_API_NAME)
    background = images[0] if images else None

    context = {
        'background_url': background['url'] if background else None,
        'background_author': background['author'] if background else None,
        'background_source': background['source'] if background else None,
    }
    return render(request, 'core/home.html', context)


def categories_view(request):
    context = {
        'categories': category_thumbnails_array(),
    }

    return render(request, 'core/categories.html', context)


def about_view(request):
    # Припустимо, search_images повертає список словників із ключами url, author, source
    images = search_images(SERVICE_API_NAME)
    background = images[0] if images else None

    context = {
        'background_url': background['url'] if background else None,
        'background_author': background['author'] if background else None,
        'background_source': background['source'] if background else None,
    }
    return render(request, 'core/about.html', context)
