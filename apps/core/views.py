import os
import random
import requests
from dotenv import load_dotenv
from django.shortcuts import render
from scripts.get_image import search_images
from django.core.paginator import Paginator

# ДОДАЙ функцію з вибору категорії і використовуй у інших, щоб не писати знову і знову те саме get_random_query(): - ось основа

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


def home_view(request):
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

    image_urls = search_images(
        'pixabay', random_category
    )  # або random.choice(['pixabay', 'pexels', 'unsplash', 'freepik'])
    background_url = image_urls[0] if isinstance(image_urls, list) else None

    context = {
        'title_of_app': 'Royalty-Free Search App',
        'background_url': background_url,
    }
    return render(request, 'core/home.html', context)


def categories_view(request):
    # Список категорій для вибору
    categories = [
        'Nature',
        'Technology',
        'Business',
        'Food',
        'Animals',
        'Sports',
        'Landscape',
        'Travel',
        'Clothes',
        'Games',
    ]

    # Отримуємо зображення для кожної категорії
    category_data = []
    for category in categories:
        # Викликаємо функцію fetch_images для кожної категорії
        image_urls = fetch_images(category, service='pixabay')
        category_data.append(
            {
                'name': category,
                'image_url': (
                    image_urls[0] if image_urls else ''
                ),  # Перше зображення або порожній рядок, якщо зображення не знайдено
            }
        )

    context = {
        'title_of_app': 'Royalty-Free Search App',
        'background_url': '',
        'categories': category_data,  # Передаємо дані категорій до шаблону
    }

    return render(request, 'core/categories.html', context)


def about_view(request):
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
    return render(request, 'core/about.html', context)
