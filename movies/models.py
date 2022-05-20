from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    overview = models.TextField()
    release_date = models.TextField()
    vote_average = models.FloatField()
    poster_path = models.TextField()
    backdrop_path = models.TextField()
    adult = models.BooleanField()
    genre = models.TextField()
    video_url = models.TextField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)