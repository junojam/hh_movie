from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
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


class Director(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_directors')
    name = models.TextField()
    profile_path = models.TextField(null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Actor(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_actors')
    name = models.TextField()
    profile_path = models.TextField(null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    character = models.TextField()