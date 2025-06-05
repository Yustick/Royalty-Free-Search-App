import random
from django.shortcuts import render
from scripts.get_image import search_images

# Create your views here.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматичний вхід
            return redirect('gallery')  # перенаправлення в галерею
    else:
        form = UserCreationForm()

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
        'form': form,  # додаємо форму до контексту
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gallery')  # перенаправлення після входу
    else:
        form = AuthenticationForm()

    # Створюємо випадкові запити для категорій
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

    # Об'єднуємо контекст для шаблону
    context = {
        'title_of_app': 'Royalty-Free Search App',
        'background_url': background_url,
        'form': form,  # передаємо форму в шаблон
    }

    return render(request, 'accounts/login.html', context)
