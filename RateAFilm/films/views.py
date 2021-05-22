from RateAFilm import settings
from django.shortcuts import render, get_object_or_404, redirect
from films.models import Film, Genre, Rating
from django.shortcuts import redirect
from films.forms import UploadFileForm, CreateRating
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv, io, json
from py2neo import Graph, Node, Relationship, NodeMatcher


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
    countries = [country['name'] for country in json.loads(film.country.replace("'", '"'))]
    genres = [i['genreName'] for i in film.genres]

    return render(request, 'film.html', {'film': film, 'countries': ', '.join(countries), 'genres': ', '.join(genres)})


def list_user_ratings(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login', request.path))
    user = request.user
    ratings = Rating.objects.all().filter(user=user.id)

    films_id = [rating.film for rating in ratings]

    films = [Film.objects.get(id=i) for i in films_id]

    elements = zip(films, ratings)

    return render(request, 'ratings.html', {'elements': elements})


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

            graph = Graph(scheme=settings.NEO4J_SCHEME, host=settings.NEO4J_HOST, port=settings.NEO4J_PORT, user=settings.NEO4J_USER, password=settings.NEO4J_PASSWORD)
            matcher = NodeMatcher(graph)

            ratings = Rating.objects.filter(user=user.id, film=film.id).count()

            if ratings != 0:
                Rating.objects.filter(user=user.id, film=film.id).delete()
                graph.evaluate('MATCH (u:User {id:' + str(user.id) + '})-[r:RATES]->(f:Film {id:' + str(film.id) + '}) DELETE r')

            new_rating = Rating.objects.create(user=user.id, film=film.id, rating=rating)

            node_user = matcher.match('User', id=int(user.id)).first()

            if node_user is None:
                node_user = Node('User', id=int(user.id))
                graph.create(node_user)

            node_film = matcher.match('Film', id=int(film.id)).first()

            if node_film is None:
                node_film = Node('Film', id=int(film.id))
                graph.create(node_film)

            relation_rating = Relationship(node_user, 'RATES', node_film, rating=float(rating))
            graph.create(relation_rating)

            return redirect('/films/' + str(film.id))
    return render(request, 'create_rating.html', {'formulario': formulario, 'film_name': film_name})


def upload_films(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            populate_films(request)
            populate_ratings(request)
            return redirect('/')
    else:
        form = UploadFileForm()

    return render(request, 'file_upload.html', {'form': form})


def populate_films(request):
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
                img = row['poster_path']

                genres = [(genre['id'], genre['name']) for genre in json.loads(row['genres'].replace("'", '"'))]
                movies_genres = []
                for genre in genres:
                    try:
                        g = Genre.objects.get(id=genre[0])

                    except Genre.DoesNotExist:
                        g = Genre.objects.create(id=genre[0], genreName=genre[1])

                    movies_genres.append(g)

                Film.objects.create(id=id, name=name, releaseDate=releaseDate, country=country, img=img, genres=movies_genres)


def populate_ratings(request):
    with io.TextIOWrapper(request.FILES['ratings'].file, encoding='utf8') as ratings_csv:
        Rating.objects.all().delete()

        reader = csv.DictReader(ratings_csv)
        graph = Graph(scheme=settings.NEO4J_SCHEME, host=settings.NEO4J_HOST, port=settings.NEO4J_PORT,
                      user=settings.NEO4J_USER, password=settings.NEO4J_PASSWORD)
        matcher = NodeMatcher(graph)

        graph.run('MATCH (n) DETACH DELETE n')
        cont = 0
        for row in reader:
            f = Film.objects.filter(id=row['movieId']).count()

            if f != 0:
                user = row['userId']
                film = row['movieId']
                rating = row['rating']
                Rating.objects.create(user=user, film=film, rating=rating)

                node_user = matcher.match('User', id=int(user)).first()

                if node_user is None:
                    node_user = Node('User', id=int(user))
                    graph.create(node_user)

                node_film = matcher.match('Film', id=int(film)).first()

                if node_film is None:
                    node_film = Node('Film', id=int(film))
                    graph.create(node_film)

                relation_rating = Relationship(node_user, 'RATES', node_film, rating=float(rating))
                graph.create(relation_rating)
                cont += 1

            if cont >= 20000:
                break
