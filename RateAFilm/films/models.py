#encoding:utf-8
from djongo import models
    
    
class Genre(models.Model):
 #   _id = models.ObjectIdField()
    genreName = models.CharField(max_length=20)
    objects=models.DjongoManager() 
    def __str__(self):
        return self.genreName   

class Country(models.Model):
#    _id = models.ObjectIdField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Film(models.Model):
#    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    releaseDate = models.DateField(null=True, blank=True)
    country= models.ForeignKey('Country',on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre)
    objects=models.DjongoManager()
    
    def __str__(self):
        return self.name




# Create your models here.
