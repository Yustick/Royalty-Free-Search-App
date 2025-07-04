from django.contrib.auth.models import User
from django.db import models


class SavedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='untitled_image')
    image_url = models.URLField()
    saved_at = models.DateTimeField(auto_now_add=True)
    image_hash = models.CharField(max_length=64, unique=True, null=False, blank=False, default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'image_hash'], name='unique_image_hash_per_user'
            ),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.name} - {self.saved_at} - {self.image_url}'
