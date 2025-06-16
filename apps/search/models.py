from django.db import models
from django.contrib.auth.models import User


class SavedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='untitled_image')
    image_url = models.URLField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.name} - {self.image_url}'
