from django.shortcuts import render
from scripts.get_image import (
    search_images,
    random_category,
    category_thumbnails_array,
    fetch_images,
)
from django.core.paginator import Paginator


def search_view(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        # Пошук зображень за допомогою вибраного сервісу
        image_urls = fetch_images(search_query, service='pixabay')
    else:
        image_urls = []  # Повертаємо порожній список, якщо запит порожній

    # Пагінація: по 18 зображень на сторінку (3 ряди по 6 стовпчиків)
    paginator = Paginator(image_urls, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title_of_app': 'Royalty-Free Search App',
        'search_query': search_query,
        'page_obj': page_obj,
    }

    return render(request, 'search/search.html', context)
