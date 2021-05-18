#encoding:utf-8
from djongo import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
    
    
class Genre(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    genreName = models.CharField(max_length=20)
    objects = models.DjongoManager()

    def __str__(self):
        return self.genreName

    def __getitem__(self, name):
        return getattr(self, name)


class Film(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    releaseDate = models.CharField(max_length=10000)
    country = models.CharField(max_length=200)
    genres = models.ArrayField(model_container=Genre)
    objects = models.DjongoManager()
    
    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.PositiveIntegerField()
    film = models.PositiveIntegerField()
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    objects = models.DjongoManager()

    def __str__(self):
        return str(self.user) + "->" + str(self.film) + "->" + str(self.rating)
