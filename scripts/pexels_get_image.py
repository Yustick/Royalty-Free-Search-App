import os
import requests
from dotenv import load_dotenv

# Завантаження змінних середовища з .env
load_dotenv()

# Отримуємо API-ключ з .env
API_KEY = os.getenv("PEXELS_API_KEY")

# Перевірка, чи був правильно отриманий API-ключ
if not API_KEY:
    print("API-ключ не знайдено! Переконайтеся, що ви додали його в .env файл.")
    exit()


def search_images(search_query):
    """
    Функція для пошуку зображень на Pexels API.

    :param search_query: Запит для пошуку (наприклад, 'landscape')
    :return: URL першого знайденого зображення або повідомлення про помилку.
    """
    url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=1"

    # Відправка запиту до API
    response = requests.get(url, headers={"Authorization": API_KEY})

    # Перевірка на успіх запиту
    if response.status_code == 200:
        data = response.json()

        # Якщо знайдено хоча б одне зображення
        if 'photos' in data and data['photos']:
            # Отримуємо URL великого зображення
            image_url = data['photos'][0]['src']['original']
            return image_url
        else:
            return "Зображення не знайдено за вашим запитом."
    else:
        return f"Помилка запиту до API: {response.status_code}"


# Приклад виклику функції
if __name__ == "__main__":
    search_query = "landscape"  # Ви можете змінити запит
    image_url = search_images(search_query)
    print(f"URL великого зображення: {image_url}")
