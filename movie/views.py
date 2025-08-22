from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64

from .models import Movie
# Create your views here.

def home(request):
    #return render(request, 'home.html', {'name':'Samuel Samper'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    #return HttpResponse('<h1>About Movie Reviews</h1><p>This is a project to review movies.</p>')
    return render(request, 'about.html', {'name':'Samuel Samper'})

def statistics_view(request):
    matplotlib.use('Agg')
    
    # ============ GRÁFICA POR AÑOS ============
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') 
    # Obtener todos los años de las películas
    movie_counts_by_year = {} 
    # Crear un diccionario para almacenar la cantidad de películas por año
    for year in years: 
        # Contar la cantidad de películas por año
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5 # Ancho de las barras
    bar_spacing = 0.5 # Separación entre las barras
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras

    # Crear la gráfica de barras por años
    plt.figure(figsize=(12, 6))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica de años en un objeto BytesIO
    buffer_years = io.BytesIO()
    plt.savefig(buffer_years, format='png')
    buffer_years.seek(0)
    plt.close()

    # Convertir la gráfica de años a base64
    image_png_years = buffer_years.getvalue()
    buffer_years.close()
    graphic_years = base64.b64encode(image_png_years)
    graphic_years = graphic_years.decode('utf-8')

    # ============ GRÁFICA POR GÉNEROS ============
    # Obtener todas las películas con género
    movies = Movie.objects.exclude(genre__isnull=True).exclude(genre='')
    
    # Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}
    
    for movie in movies:
        # Obtener solo el primer género (dividir por coma y tomar el primero)
        first_genre = movie.genre.split(',')[0].strip()
        
        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1
    
    # Ordenar por cantidad de películas (descendente)
    sorted_genres = dict(sorted(movie_counts_by_genre.items(), key=lambda x: x[1], reverse=True))
    
    bar_width_genre = 0.6
    bar_positions_genre = range(len(sorted_genres))
    
    # Crear la gráfica de barras por géneros
    plt.figure(figsize=(12, 6))
    plt.bar(bar_positions_genre, sorted_genres.values(), width=bar_width_genre, align='center')
    
    # Personalizar la gráfica
    plt.title('Movies per Genre (First Genre Only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, sorted_genres.keys(), rotation=45, ha='right')
    
    # Ajustar el espaciado
    plt.tight_layout()
    
    # Guardar la gráfica de géneros en un objeto BytesIO
    buffer_genres = io.BytesIO()
    plt.savefig(buffer_genres, format='png')
    buffer_genres.seek(0)
    plt.close()
    
    # Convertir la gráfica de géneros a base64
    image_png_genres = buffer_genres.getvalue()
    buffer_genres.close()
    graphic_genres = base64.b64encode(image_png_genres)
    graphic_genres = graphic_genres.decode('utf-8')

    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic_years': graphic_years,
        'graphic_genres': graphic_genres
    })

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

    # Renderizar la plantilla statistics.html con ambas gráficas
    return render(request, 'statistics.html', {
        'graphic_years': graphic_years,
        'graphic_genres': graphic_genres
    })