from django.shortcuts import render, get_object_or_404, redirect
from films.models import Film

def index(request): 
    return render(request,'index.html')

def list_films(request):
    films=Film.objects.all()
    return render(request,'films.html', {'films':films})
# Create your views here.
