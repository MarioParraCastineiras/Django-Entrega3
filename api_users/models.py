from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    music_style = models.CharField(max_length=1000, unique = False)
    preferred_artists = models.CharField(max_length = 500, unique = False)
    liked_songs = models.CharField(max_length=1000, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created_at']
