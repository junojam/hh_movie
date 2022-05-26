from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Actor(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_actors')
    name = models.TextField()
    profile_path = models.TextField(null=True)
    
    def __str__(self):
        return self.name

class Director(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_directors')
    name = models.TextField()
    profile_path = models.TextField(null=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=20)
    overview = models.TextField()
    release_date = models.TextField()
    vote_average = models.FloatField()
    poster_path = models.TextField()
    backdrop_path = models.TextField(null=True)
    adult = models.BooleanField()
    genre = models.TextField()
    video_url = models.TextField(null=True)
    actors = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class Score(models.Model):
    star = models.FloatField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)