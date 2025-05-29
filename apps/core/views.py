from django.shortcuts import render
from scripts.get_image import search_images

# ЗРОБИ ЯКИЙСЬ ВИБІР МІЖ АПІШКАМИ

# Create your views here.


# def base_view(request):
#     return render(
#         request,
#         'core/index.html',
#     )


# def categories_view(request):
#     return render(
#         request,
#         'core/categories.html',
#     )


# def about_view(request):
#     return render(
#         request,
#         'core/about.html',
#     )


# def contact_view(request):
#     return render(
#         request,
#         'core/contact.html',
#     )


# def search_view(request):
#     image_url = None
#     search_query = None

#     if request.method == "GET" and "search_query" in request.GET:
#         search_query = request.GET["search_query"]
#         image_url = search_images('pixabay', search_query)

#     return render(
#         request,
#         'core/index.html',
#         {'image_url': image_url, 'search_query': search_query},
#     )

# import os
# import random
# import requests
# from dotenv import load_dotenv
# from django.shortcuts import render

# # Завантаження змінних середовища з .env
# load_dotenv()

# # Отримуємо API-ключі для різних сервісів
# API_KEYS = {
#     'pixabay': os.getenv('PIXABAY_API_KEY'),
#     'pexels': os.getenv('PEXELS_API_KEY'),
#     'unsplash': os.getenv('UNSPLASH_ACCESS_KEY_API'),
#     'freepik': os.getenv('FREEPIK_API_KEY'),
# }

# # Перевірка наявності ключів
# for key, value in API_KEYS.items():
#     if not value:
#         print(f"API-ключ для {key} не знайдено! Переконайтеся, що ви додали його в .env файл.")

# def fetch_images(query, service='unsplash'):
#     image_urls = []

#     if service == 'unsplash':
#         url = f"https://api.unsplash.com/photos/random?query={query}&client_id={API_KEYS['unsplash']}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             image_urls = [image['urls']['regular'] for image in data]

#     elif service == 'pexels':
#         url = f"https://api.pexels.com/v1/search?query={query}&per_page=20"
#         headers = {"Authorization": API_KEYS['pexels']}
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             data = response.json()
#             image_urls = [photo['src']['original'] for photo in data['photos']]

#     elif service == 'pixabay':
#         url = f"https://pixabay.com/api/?key={API_KEYS['pixabay']}&q={query}&image_type=photo"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             image_urls = [hit['largeImageURL'] for hit in data['hits']]

#     elif service == 'freepik':
#         url = f"https://api.freepik.com/v2/search/?q={query}&api_key={API_KEYS['freepik']}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             image_urls = [item['image_url'] for item in data['data']]

#     return image_urls[:20]  # Повертати не більше 20 зображень

# def search_view(request):
#     search_query = request.GET.get('search_query', '')
#     image_urls = []

#     if search_query:
#         # Вибір випадкового API для пошуку
#         services = ['unsplash', 'pexels', 'pixabay', 'freepik']
#         random_service = random.choice(services)

#         image_urls = fetch_images(search_query, service=random_service)

#     return render(request, 'search_results.html', {
#         'search_query': search_query,
#         'image_urls': image_urls
#     })
# _______________________________________________
import os
import random
import requests
from dotenv import load_dotenv
from django.shortcuts import render

# Завантаження змінних середовища з .env
load_dotenv()

# Отримуємо API-ключі для різних сервісів
API_KEYS = {
    'pixabay': os.getenv('PIXABAY_API_KEY'),
    'pexels': os.getenv('PEXELS_API_KEY'),
    'unsplash': os.getenv('UNSPLASH_ACCESS_KEY_API'),
    'freepik': os.getenv('FREEPIK_API_KEY'),
}

# Перевірка наявності ключів
for key, value in API_KEYS.items():
    if not value:
        print(
            f"API-ключ для {key} не знайдено! Переконайтеся, що ви додали його в .env файл."
        )


def fetch_images(query, service='pixabay'):
    image_urls = []

    if service == 'unsplash':
        url = f"https://api.unsplash.com/photos/random?query={query}&client_id={API_KEYS['unsplash']}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    image_urls = [image['urls']['regular'] for image in data]
                else:
                    print(f"Unexpected data format from Unsplash: {data}")
            except Exception as e:
                print(f"Error parsing JSON from Unsplash: {e}")

    elif service == 'pexels':
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=20"
        headers = {"Authorization": API_KEYS['pexels']}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict) and 'photos' in data:
                    image_urls = [photo['src']['original'] for photo in data['photos']]
                else:
                    print(f"Unexpected data format from Pexels: {data}")
            except Exception as e:
                print(f"Error parsing JSON from Pexels: {e}")

    elif service == 'pixabay':
        url = f"https://pixabay.com/api/?key={API_KEYS['pixabay']}&q={query}&image_type=photo"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict) and 'hits' in data:
                    image_urls = [hit['largeImageURL'] for hit in data['hits']]
                else:
                    print(f"Unexpected data format from Pixabay: {data}")
            except Exception as e:
                print(f"Error parsing JSON from Pixabay: {e}")

    elif service == 'freepik':
        url = f"https://api.freepik.com/v2/search/?q={query}&api_key={API_KEYS['freepik']}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict) and 'data' in data:
                    image_urls = [item['image_url'] for item in data['data']]
                else:
                    print(f"Unexpected data format from Freepik: {data}")
            except Exception as e:
                print(f"Error parsing JSON from Freepik: {e}")

    return image_urls[:20]  # Повертати не більше 20 зображень


def base_view(request):
    # Створимо випадкові запити для категорій
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

    image_urls = fetch_images(random_category)

    return render(
        request,
        'core/index.html',
        {'image_urls': image_urls, 'random_category': random_category},
    )


def categories_view(request):
    # Ви можете повернути список категорій для вибору
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

    return render(request, 'categories.html', {'categories': categories})


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


def search_view(request):
    search_query = request.GET.get('search_query', '')
    image_urls = []

    if search_query:
        # Вибір випадкового API для пошуку
        services = ['unsplash', 'pexels', 'pixabay', 'freepik']
        random_service = random.choice(services)

        image_urls = fetch_images(search_query, service=random_service)

    return render(
        request,
        # 'search_results.html',
        'core/index.html',
        {'search_query': search_query, 'image_urls': image_urls},
    )
