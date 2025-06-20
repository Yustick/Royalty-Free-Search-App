import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()

# API keys from .env
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_ACCESS_KEY_API')
FREEPIK_API_KEY = os.getenv('FREEPIK_API_KEY')

if not PIXABAY_API_KEY or not PEXELS_API_KEY or not UNSPLASH_API_KEY or not FREEPIK_API_KEY:
    print('One or more API keys not found! Make sure you added them to the .env file.')
    exit()

QUERIES_CATEGORIES = [
    'Technology',
    'Business',
    'Food',
    'Animals',
    'Sports',
    'Landscape',
    'Travel',
    'Clothes',
    'Games',
    'City',
    'Abstract',
    'Ocean',
    'Mountain',
    'Forest',
    'Night sky',
    'Flowers',
]


def get_random_topic():
    """
    Returns a random search query from a predefined list.

    :return: A random string representing a topic
    """
    return random.choice(QUERIES_CATEGORIES)


def fetch_images(query, service='pixabay', limit=180):
    """
    Retrieves images with metadata (URL, author, source).

    :return: List of dicts with 'url', 'author', 'source'
    """
    images = []

    if service == 'unsplash':
        url = f'https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_API_KEY}&count={limit}'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    for item in data:
                        images.append(
                            {
                                'url': item['urls']['regular'],
                                'author': item['user']['name'],
                                'source': 'Unsplash',
                            }
                        )
            except Exception as e:
                print(f'Error parsing JSON from Unsplash: {e}')

    elif service == 'pexels':
        url = f'https://api.pexels.com/v1/search?query={query}&per_page={limit}'
        headers = {'Authorization': PEXELS_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                for photo in data.get('photos', []):
                    images.append(
                        {
                            'url': photo['src']['original'],
                            'author': photo['photographer'],
                            'source': 'Pexels',
                        }
                    )
            except Exception as e:
                print(f'Error parsing JSON from Pexels: {e}')

    elif service == 'pixabay':
        limit = max(3, limit)
        url = f'https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page={limit}'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                for hit in data.get('hits', []):
                    images.append(
                        {
                            'url': hit['largeImageURL'],
                            'author': hit.get('user', 'Unknown'),
                            'source': 'Pixabay',
                        }
                    )
            except Exception as e:
                print(f'Error parsing JSON from Pixabay: {e}')

    elif service == 'freepik':
        url = (
            f'https://api.freepik.com/v2/search/?q={query}&api_key={FREEPIK_API_KEY}&limit={limit}'
        )
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                for item in data.get('data', []):
                    images.append(
                        {
                            'url': item['image_url'],
                            'author': item.get('author', 'Unknown'),
                            'source': 'Freepik',
                        }
                    )
            except Exception as e:
                print(f'Error parsing JSON from Freepik: {e}')

    return images[:limit]


def search_images(service, query=None, limit=5):
    """
    Wrapper for retrieving images with metadata.

    :return: List of dicts with 'url', 'author', 'source'
    """
    query = query or get_random_topic()
    return fetch_images(query, service=service, limit=limit)


def category_thumbnails_array():
    """
    Forms a list of categories with one image (thumbnail) in each.

    :return: List of dicts with 'name' and 'image_url'
    """
    category_data = []
    for category in QUERIES_CATEGORIES:
        image = fetch_images(category, service='pixabay', limit=1)
        category_data.append(
            {
                'name': category,
                'image_url': image[0]['url'] if image else '',
            }
        )
    return category_data
