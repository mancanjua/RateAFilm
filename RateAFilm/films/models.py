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


class Country(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Film(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    releaseDate = models.DateField(null=True, blank=True)
    country = models.EmbeddedField(model_container=Country)
    genres = models.ArrayReferenceField(to=Genre)
    objects = models.DjongoManager()
    
    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.PositiveIntegerField()
    film = models.PositiveIntegerField()
    date = models.DateField(null=True, blank=True)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return str(self.user) + "->" + str(self.film) + "->" + str(self.rating)
