import os
import requests
from dotenv import load_dotenv

# МОЖЛИВО ТРЕБА ПЕРЕПИСАТИ КОД, БО АПІ ПРАЦЮЄ ТУТ НЕ ТАК

# Завантаження змінних середовища з .env
load_dotenv()

# Отримуємо API-ключ з .env
API_KEY = os.getenv("FREEPIK_API_KEY")

# Перевірка, чи був правильно отриманий API-ключ
if not API_KEY:
    print("API-ключ не знайдено! Переконайтеся, що ви додали його в .env файл.")
    exit()

# Параметри запиту
search_query = "landscape"  # Ви можете змінити запит
url = f"https://api.freepik.com/v2/search/?q={search_query}&api_key={API_KEY}"

# Відправка запиту до API
response = requests.get(url)

# Перевірка на успіх запиту
if response.status_code == 200:
    data = response.json()

    # Якщо знайдено хоча б одне зображення
    if 'data' in data and data['data']:
        # Отримуємо URL великого зображення
        image_url = data['data'][0]['image_url']
        print("URL великого зображення:", image_url)
    else:
        print("Зображення не знайдено за вашим запитом.")
else:
    print(f"Помилка запиту до API: {response.status_code}")
