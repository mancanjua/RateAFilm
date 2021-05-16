from django.shortcuts import render, get_object_or_404, redirect
from films.models import Film, Rating
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from films.forms import UploadFileForm

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
            populate_data(request.FILES['movies'], request.FILES['ratings'])
            return redirect('/')
    else:
        form = UploadFileForm()

    return render(request, 'file_upload.html', {'form': form})


def populate_data(movies, ratings):
    pass
