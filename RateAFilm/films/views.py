from django.shortcuts import render, get_object_or_404, redirect
from films.models import Film, Rating, Genre
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from films.forms import UploadFileForm
import csv, io, json

def index(request): 
    return render(request,'index.html')

def list_films(request):
    films=Film.objects.all()
    return render(request,'films.html', {'films':films})
def show_film(request, pk):

    film = get_object_or_404(Film,id=pk)


    return render(request,'film.html', {'film':film})
# Create your views here.


def list_user_ratings(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login', request.path))
    user = request.user
    ratings = Rating.objects.filter(user=user)

    return render(request, 'ratings.html', {'ratings':ratings})


def upload_films(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            populate_data(request)
            return redirect('/')
    else:
        form = UploadFileForm()

    return render(request, 'file_upload.html', {'form': form})


def populate_data(request):
    with io.TextIOWrapper(request.FILES['movies'].file, encoding='utf8') as movies_csv:
        reader = csv.DictReader(movies_csv)
        for row in reader:
            genres = [genre['name'] for genre in json.loads(row['genres'].replace("'", '"'))]
            movies_genres = []
            for genre in genres:
                g = Genre.objects.get(genreName=genre)

                if g is None:
                    g = Genre.objects.create(genreName=genre)

                movies_genres.append(g)


def test(request):
    genres = ['prueba1', 'prueba2']
