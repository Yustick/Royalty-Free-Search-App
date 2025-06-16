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

from django.urls import path
from . import views

urlpatterns = [
    path('gallery/', views.gallery_view, name='gallery'),
    path(
        'gallery/download-saved-image/<int:image_id>/',
        views.download_image,
        name='download_saved_image',
    ),
    path(
        'gallery/delete-image/<int:image_id>/',
        views.delete_saved_image,
        name='delete_saved_image',
    ),
    path('gallery/edit/', views.process_image_edit, name='process_image_edit'),
    path(
        'gallery/edit-image/<int:image_id>/',
        views.edit_image_view,
        name='edit_image_view',
    ),
]
