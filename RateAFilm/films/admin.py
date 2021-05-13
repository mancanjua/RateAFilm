from django.contrib import admin
from .models import Film, Genre, Country, Rating
admin.site.register(Film)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Rating)
# Register your models here.
