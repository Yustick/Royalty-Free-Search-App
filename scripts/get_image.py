import os
import random

import requests
from dotenv import load_dotenv

load_dotenv()

# Getting API keys from .env
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
    """Function for generating random queries"""
    return random.choice(QUERIES_CATEGORIES)


def fetch_images(query, service='pixabay', limit=20):
    """A universal function for retrieving images from various APIs."""
    image_urls = []

    if service == 'unsplash':
        url = f'https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_API_KEY}&count={limit}'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    image_urls = [image['urls']['regular'] for image in data]
            except Exception as e:
                print(f'Error parsing JSON from Unsplash: {e}')

    elif service == 'pexels':
        url = f'https://api.pexels.com/v1/search?query={query}&per_page={limit}'
        headers = {'Authorization': PEXELS_API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                if 'photos' in data:
                    image_urls = [photo['src']['original'] for photo in data['photos']]
            except Exception as e:
                print(f'Error parsing JSON from Pexels: {e}')

    elif service == 'pixabay':
        limit = max(3, limit)  # API requirement, minimum photos
        url = f'https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page={limit}'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                if 'hits' in data:
                    image_urls = [hit['largeImageURL'] for hit in data['hits']]
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
                if 'data' in data:
                    image_urls = [item['image_url'] for item in data['data']]
            except Exception as e:
                print(f'Error parsing JSON from Freepik: {e}')

    return image_urls[:limit]


def search_images(service, query=None, limit=5):
    """Wrapper for quickly retrieving multiple images (default 5)."""
    query = query or get_random_topic()
    return fetch_images(query, service=service, limit=limit)


def category_thumbnails_array():
    """Forming a list of categories with one image in each."""
    category_data = []
    for category in QUERIES_CATEGORIES:
        image_urls = fetch_images(category, service='pixabay', limit=1)
        category_data.append(
            {
                'name': category,
                'image_url': image_urls[0] if image_urls else '',
            }
        )
    return category_data
