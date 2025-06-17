import os
import base64
import time
import requests
import threading
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageEnhance, ImageFilter
from apps.search.models import SavedImage
from django.views.decorators.http import require_POST, require_http_methods


@login_required
def gallery_view(request):
    saved_images = SavedImage.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(saved_images, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'gallery/gallery.html', {'page_obj': page_obj})


@require_POST
@login_required
def download_image(request, image_id):
    image = get_object_or_404(SavedImage, id=image_id, user=request.user)
    image_url = image.image_url
    name = image.name

    if not image_url or not name:
        return Http404('Image not found or invalid.')
    response = requests.get(image_url)

    if response.status_code != 200:
        return Http404('Failed to download the image.')

    file_name = f'{name}.jpg'
    response = HttpResponse(response.content, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response


@require_POST
@login_required
def delete_saved_image(request, image_id):
    image = get_object_or_404(SavedImage, id=image_id, user=request.user)
    image.delete()
    return redirect('gallery')


def delete_file_after_delay(file_path, delay_seconds=180):
    def _delete():
        time.sleep(delay_seconds)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Error deleting file {file_path}: {e}')

    threading.Thread(target=_delete).start()


@login_required
@require_http_methods(['GET'])
def edit_image_view(request, image_id):
    image = get_object_or_404(SavedImage, id=image_id, user=request.user)

    # Loading the image from the URL if it is not already saved, and then deleting it after 10 minutes so there is no garbage
    temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_downloads')
    os.makedirs(temp_path, exist_ok=True)
    # Workaround for giving different names to files is already editable,
    # because only a query is available for the name, not a unique name given by API
    filename = f'{image.name}_{image.saved_at.strftime("%Y-%m-%d_%H-%M-%S")}.jpg'
    temp_image_path = os.path.join(temp_path, filename)

    if not os.path.exists(temp_image_path):
        response = requests.get(image.image_url)
        if response.status_code == 200:
            with open(temp_image_path, 'wb') as f:
                f.write(response.content)
                delete_file_after_delay(temp_image_path, delay_seconds=600)

    image_url = f'/media/temp_downloads/{filename}'
    return render(
        request,
        'gallery/edit_image.html',
        {
            'image_url': image_url,
            'image_id': image.id,
        },
    )


@login_required
@require_http_methods(['POST'])
def process_image_edit(request):
    if request.method == 'POST':
        try:
            cropped_data = request.POST.get('cropped_data')
            brightness = float(request.POST.get('brightness', 1))
            contrast = float(request.POST.get('contrast', 1))
            grayscale = float(request.POST.get('grayscale', 0))
            sepia = float(request.POST.get('sepia', 0))
            invert = float(request.POST.get('invert', 0))
            blur = float(request.POST.get('blur', 0))
            rotate_degrees = int(request.POST.get('rotate_degrees', 0))  # 0,90,180,270
            img_format = request.POST.get('format', 'JPEG').upper()

            if not cropped_data:
                return HttpResponse('No cropped image data provided', status=400)

            # Extracting base64 from data URL
            header, base64_data = cropped_data.split(',', 1)
            img_bytes = base64.b64decode(base64_data)
            image = Image.open(BytesIO(img_bytes)).convert('RGBA')

            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)

            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)

            if grayscale > 0:
                gray_image = image.convert('L')
                gray_image = gray_image.convert('RGBA')
                image = Image.blend(image, gray_image, grayscale)

            if sepia > 0:
                sepia_image = image.convert('RGB')
                width, height = sepia_image.size
                pixels = sepia_image.load()
                for py in range(height):
                    for px in range(width):
                        r, g, b = pixels[px, py]
                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                        tr = min(255, tr)
                        tg = min(255, tg)
                        tb = min(255, tb)
                        pixels[px, py] = (tr, tg, tb)
                sepia_image = sepia_image.convert('RGBA')
                image = Image.blend(image, sepia_image, sepia)

            if invert > 0:
                inverted_image = Image.eval(image, lambda px: 255 - px)
                image = Image.blend(image, inverted_image, invert)

            if blur > 0:
                image = image.filter(ImageFilter.GaussianBlur(radius=blur))

            if rotate_degrees:
                image = image.rotate(-rotate_degrees, expand=True)

            # Convert to RGB if JPEG
            if img_format == 'JPEG':
                image = image.convert('RGB')

            buffer = BytesIO()
            image.save(buffer, format=img_format)
            buffer.seek(0)

            # Getting name of the image
            image_id = request.POST.get('image_id')
            image_name = get_object_or_404(
                SavedImage, id=image_id, user=request.user
            ).name

            response = HttpResponse(buffer, content_type=f'image/{img_format.lower()}')
            response['Content-Disposition'] = (
                f'attachment; filename="edited_{image_name}.{img_format.lower()}"'
            )
            return response

        except Exception as e:
            return HttpResponse(f'Error processing image: {str(e)}', status=500)
    else:
        return HttpResponse('Only POST allowed', status=405)
