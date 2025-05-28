import os
import requests
from dotenv import load_dotenv

# Завантаження змінних середовища з .env
load_dotenv()

# Отримуємо API-ключ з .env
API_KEY = os.getenv("UNSPLASH_ACCESS_KEY_API")

# Перевірка, чи був правильно отриманий API-ключ
if not API_KEY:
    print("API-ключ не знайдено! Переконайтеся, що ви додали його в .env файл.")
    exit()

# Параметри запиту
search_query = "landscape"  # Ви можете змінити запит
url = f"https://api.unsplash.com/photos/random?query={search_query}&client_id={API_KEY}"

# Відправка запиту до API
response = requests.get(url)

# Перевірка на успіх запиту
if response.status_code == 200:
    data = response.json()

    # Якщо знайдено хоча б одне зображення
    if data:
        # Отримуємо URL великого зображення
        image_url = data[0]['urls']['regular']
        print("URL великого зображення:", image_url)
    else:
        print("Зображення не знайдено за вашим запитом.")
else:
    print(f"Помилка запиту до API: {response.status_code}")
