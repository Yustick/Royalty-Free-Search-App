import os
import requests
import random
from dotenv import load_dotenv

# ВИКОРИСТАЙ ЦЕЙ ФАЙЛ, БО ВІН ОДИН І СКОРОЧУЄ К-СТЬ КОДУ + Є ВАРІК РАНДОМНИХ ЗОБРАЖЕНЬ

# Завантаження змінних середовища з .env
load_dotenv()

# Отримуємо API-ключі з .env
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_ACCESS_KEY_API")
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY")

# Перевірка, чи були отримані API-ключі
if (
    not PIXABAY_API_KEY
    or not PEXELS_API_KEY
    or not UNSPLASH_API_KEY
    or not FREEPIK_API_KEY
):
    print(
        "Один або кілька API-ключів не знайдено! Переконайтеся, що ви додали їх в .env файл."
    )
    exit()


def search_images(api_name, search_query=None):
    """
    Функція для пошуку зображень через різні API.

    :param api_name: Назва API для використання (наприклад, 'pixabay', 'pexels', 'unsplash', 'freepik')
    :param search_query: Запит для пошуку (наприклад, 'landscape'). Якщо не передано, генерується випадковий запит.
    :return: Список URL великих зображень або повідомлення про помилку.
    """
    if search_query is None:
        search_query = (
            get_random_query()
        )  # Генеруємо випадковий запит для обладинок чи фонового зображення

    if api_name == "pixabay":
        return search_images_pixabay(search_query)
    elif api_name == "pexels":
        return search_images_pexels(search_query)
    elif api_name == "unsplash":
        return search_images_unsplash(search_query)
    elif api_name == "freepik":
        return search_images_freepik(search_query)
    else:
        return "Невідомий API."


def get_random_query():
    """Функція для генерації випадкових запитів."""
    random_queries = [
        "landscape",
        "nature",
        "city",
        "abstract",
        "ocean",
        "mountain",
        "forest",
        "animals",
        "night sky",
        "flowers",
    ]
    return random.choice(random_queries)


def search_images_pixabay(search_query):
    """Функція для пошуку зображень на Pixabay API."""
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={search_query}&image_type=photo"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'hits' in data and data['hits']:
            return [
                hit['largeImageURL'] for hit in data['hits'][:5]
            ]  # Повертаємо перші 5 зображень
        else:
            return "Зображення не знайдено за вашим запитом."
    else:
        return f"Помилка запиту до API: {response.status_code}"


def search_images_pexels(search_query):
    """Функція для пошуку зображень на Pexels API."""
    url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=5"
    response = requests.get(url, headers={"Authorization": PEXELS_API_KEY})
    if response.status_code == 200:
        data = response.json()
        if 'photos' in data and data['photos']:
            return [photo['src']['original'] for photo in data['photos']]
        else:
            return "Зображення не знайдено за вашим запитом."
    else:
        return f"Помилка запиту до API: {response.status_code}"


def search_images_unsplash(search_query):
    """Функція для пошуку зображень на Unsplash API."""
    url = f"https://api.unsplash.com/photos/random?query={search_query}&client_id={UNSPLASH_API_KEY}&count=5"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return [image['urls']['regular'] for image in data]
        else:
            return "Зображення не знайдено за вашим запитом."
    else:
        return f"Помилка запиту до API: {response.status_code}"


def search_images_freepik(search_query):
    """Функція для пошуку зображень на Freepik API."""
    url = (
        f"https://api.freepik.com/v2/search/?q={search_query}&api_key={FREEPIK_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']:
            return [
                item.get('image_url', "Зображення не має доступного URL.")
                for item in data['data'][:5]
            ]
        else:
            return "Зображення не знайдено за вашим запитом."
    else:
        return f"Помилка запиту до API: {response.status_code}"


# Приклад виклику функції
if __name__ == "__main__":
    api_name = "pixabay"  # Змініть на 'pexels', 'unsplash' або 'freepik' для використання інших API
    image_urls = search_images(api_name)
    print(f"Зображення за запитом: {image_urls}")
