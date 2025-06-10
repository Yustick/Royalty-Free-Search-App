from django.shortcuts import render
from scripts.get_image import search_images, random_category, category_thumbnails_array

# ДОДАЙ функцію з вибору категорії і використовуй у інших, щоб не писати знову і знову те саме get_random_query(): - ось основа
# title_of_app - прибери можливо - захардькодь


def home_view(request):
    image_urls = search_images(
        'pixabay', random_category()
    )  # або random.choice(['pixabay', 'pexels', 'unsplash', 'freepik'])
    background_url = image_urls[0] if isinstance(image_urls, list) else None

    context = {
        'title_of_app': 'Royalty-Free Search App',
        'background_url': background_url,
    }
    return render(request, 'core/home.html', context)


def categories_view(request):
    context = {
        'title_of_app': 'Royalty-Free Search App',
        'background_url': '',
        'categories': category_thumbnails_array(),  # Передаємо дані категорій до шаблону
    }

    return render(request, 'core/categories.html', context)


def about_view(request):
    image_urls = search_images(
        'pixabay', random_category()
    )  # або random.choice(['pixabay', 'pexels', 'unsplash', 'freepik'])
    background_url = image_urls[0] if isinstance(image_urls, list) else None

    context = {
        'title_of_app': 'Royalty-Free Search App',
        'background_url': background_url,
    }
    return render(request, 'core/about.html', context)
