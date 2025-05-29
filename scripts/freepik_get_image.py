import os
import requests
from dotenv import load_dotenv

# Завантаження змінних середовища з .env
load_dotenv()

# Отримуємо API-ключ з .env
API_KEY = os.getenv("FREEPIK_API_KEY")

# Перевірка, чи був правильно отриманий API-ключ
if not API_KEY:
    print("API-ключ не знайдено! Переконайтеся, що ви додали його в .env файл.")
    exit()


def search_images(search_query):
    """
    Функція для пошуку зображень на Freepik API.

    :param search_query: Запит для пошуку (наприклад, 'landscape')
    :return: URL великого зображення або повідомлення про помилку.
    """
    url = f"https://api.freepik.com/v2/search/?q={search_query}&api_key={API_KEY}"

    # Відправка запиту до API
    response = requests.get(url)

    # Перевірка на успіх запиту
    if response.status_code == 200:
        data = response.json()

        # Якщо знайдено хоча б одне зображення
        if 'data' in data and data['data']:
            # Отримуємо URL першого зображення (якщо це вектор чи фото)
            image_url = data['data'][0].get(
                'image_url'
            )  # Може бути 'image_url' чи інший ключ залежно від відповіді
            if image_url:
                return image_url
            else:
                return "Зображення не має доступного URL."
        else:
            return "Зображення не знайдено за вашим запитом."
    else:
        return f"Помилка запиту до API: {response.status_code}"


# Приклад виклику функції
if __name__ == "__main__":
    search_query = "landscape"  # Ви можете змінити запит
    image_url = search_images(search_query)
    print(f"URL великого зображення: {image_url}")
