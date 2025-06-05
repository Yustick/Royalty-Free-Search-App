"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from apps.core import views as core_views
from apps.accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # тут можна рандомні набір запитів, який повертатиме з два десятки картинок,
    # що відображатимуться на головній перед запитом АБО краще щоб це були категорії
    path('RoyaltyFreeSearchApp/', core_views.home_view, name='home'),
    path(
        'RoyaltyFreeSearchApp/categories', core_views.categories_view, name='categories'
    ),
    path('RoyaltyFreeSearchApp/about', core_views.about_view, name='about'),
    path('RoyaltyFreeSearchApp/gallery', core_views.gallery_view, name='gallery'),
    path('RoyaltyFreeSearchApp/search', core_views.search_view, name='search_view'),
    path('register/', accounts_views.register, name='register'),
    path('login/', accounts_views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
