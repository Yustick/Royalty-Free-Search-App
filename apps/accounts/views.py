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

    context = {
        'title_of_app': 'Royalty-Free Search App',
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

    # Об'єднуємо контекст для шаблону
    context = {
        'title_of_app': 'Royalty-Free Search App',
        'form': form,  # передаємо форму в шаблон
    }

    return render(request, 'accounts/login.html', context)
