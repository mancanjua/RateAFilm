"""RateAFilm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from films import views
from register import views as vr

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('films/', views.list_films, name='film-list'),
    path('films/<int:pk>', views.show_film, name='film-detail'),
    path('films/<int:pk>/create_rating', views.create_rating, name='create-rating'),
    path('ratings/', views.list_user_ratings),
    path('register', vr.register, name="register"),
    path('', include('django.contrib.auth.urls')),
    path('import', views.upload_films, name='upload')
]
