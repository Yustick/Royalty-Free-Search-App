import requests
import hashlib
from django.shortcuts import render
from scripts.get_image import fetch_images
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import SavedImage
from django.http import HttpResponse, Http404, HttpResponseBadRequest

SERVICE_API_NAME = 'pixabay'


def search_view(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        image_urls = fetch_images(search_query, service=SERVICE_API_NAME)
    else:
        image_urls = []

    paginator = Paginator(image_urls, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'search_query': search_query,
        'page_obj': page_obj,
    }

    return render(request, 'search/search.html', context)


@require_POST
@login_required
def save_image_to_gallery(request):
    image_url = request.POST.get('image_url')
    search_query = request.POST.get('search_query')

    if not image_url or not search_query:
        return HttpResponseBadRequest(
            'Missing required fields: image_url or search_query.'
        )

    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            return HttpResponseBadRequest('Failed to retrieve the image from the URL.')
        image_data = response.content
    except requests.exceptions.RequestException as e:
        return HttpResponseBadRequest(f'Error fetching image: {e}')

    image_hash = hashlib.md5(image_data).hexdigest()

    if SavedImage.objects.filter(user=request.user, image_hash=image_hash).exists():
        return HttpResponseBadRequest('This image is already saved in your gallery.')

    try:
        SavedImage.objects.create(
            user=request.user,
            image_url=image_url,
            name=search_query,
            image_hash=image_hash,
        )
    except Exception as e:
        return HttpResponseBadRequest(f'Error saving image: {e}')

    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def download_image(request):
    image_url = request.POST.get('image_url')
    name = request.POST.get('search_query')

    if not image_url or not name:
        return Http404('Image not found or invalid.')

    response = requests.get(image_url)
    if response.status_code != 200:
        return Http404('Failed to download the image.')

    file_name = f'{name}.jpg'

    response = HttpResponse(response.content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response
