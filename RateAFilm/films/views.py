from django.shortcuts import render, get_object_or_404, redirect
from films.models import Film, Genre, Rating
from django.shortcuts import redirect
from films.forms import UploadFileForm, CreateRating
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv, io, json



def index(request): 
    return render(request, 'index.html')


def list_films(request):
    films = Film.objects.all()
    paginator = Paginator(films, 1000)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    films_page = paginator.get_page(page_number)
    return render(request, 'films.html', {'films_page': films_page})


def show_film(request, pk):
    film = get_object_or_404(Film, id=pk)
    return render(request, 'film.html', {'film': film})


def list_user_ratings(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login', request.path))
    user = request.user
    ratings = Rating.objects.all().filter(user=user.id)

    return render(request, 'ratings.html', {'ratings': ratings})

def create_rating(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login', request.path))
    formulario = CreateRating()
    film_name = Film.objects.get(id=pk)
    if request.method == 'POST':
        formulario = CreateRating(request.POST)
        if formulario.is_valid():
            film = get_object_or_404(Film, id=pk)
            user = request.user
            rating = formulario.cleaned_data['rating']
            new_rating = Rating.objects.create(user=user.id, film=film.id, rating=rating)
            return redirect('/')
    return render(request, 'create_rating.html', {'formulario': formulario, 'film_name': film_name})



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
        Genre.objects.all().delete()
        Film.objects.all().delete()

        reader = csv.DictReader(movies_csv)

        for row in reader:
            if row['adult'] != 'False' and row['adult'] != 'True':
                continue

            f = Film.objects.filter(id=row['id']).count()

            if f == 0:
                country = row['production_countries']
                releaseDate = row['release_date']
                name = row['original_title']
                id = row['id']

                genres = [(genre['id'], genre['name']) for genre in json.loads(row['genres'].replace("'", '"'))]
                movies_genres = []
                for genre in genres:
                    try:
                        g = Genre.objects.get(id=genre[0])

                    except Genre.DoesNotExist:
                        g = Genre.objects.create(id=genre[0], genreName=genre[1])

                    movies_genres.append(g)

                Film.objects.create(id=id, name=name, releaseDate=releaseDate, country=country, genres=movies_genres)

    with io.TextIOWrapper(request.FILES['ratings'].file, encoding='utf8') as ratings_csv:
        Rating.objects.all().delete()

        reader = csv.DictReader(ratings_csv)

        for row in reader:
            user = row['userId']
            film = row['movieId']
            rating = row['rating']

            Rating.objects.create(user=user, film=film, rating=rating)
