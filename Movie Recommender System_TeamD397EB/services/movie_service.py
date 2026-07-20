# Movie service - orchestrates online/offline modes
import time
from services import tmdb_service
from models import movie_model, user_model

# Cache internet status for 30 seconds
_online_cache = {'status': None, 'time': 0}

# Mood to genre mapping
MOOD_GENRES = {
    'happy': ['Comedy'],
    'sad': ['Drama'],
    'funny': ['Comedy'],
    'romantic': ['Romance'],
    'thriller': ['Thriller'],
    'horror': ['Horror'],
    'adventure': ['Action', 'Adventure'],
    'family': ['Family', 'Animation'],
    'mystery': ['Mystery', 'Crime'],
    'scifi': ['Sci-Fi'],
}


def is_online():
    """Always return False to force offline mode and use local DB for images."""
    return False


def search(query, user_id=1, year=''):
    """Search movies - online uses TMDB, offline uses local DB."""
    # Save search history
    user_model.add_search_history(user_id, query)

    if is_online():
        results = tmdb_service.search_movies(query)
        if year and results:
            results = [m for m in results if m.get('release_date') and m['release_date'].startswith(year)]
        if results:
            return results

    # Fallback to local database
    local_movies = movie_model.search_movies_local(query, year)
    return _format_local_movies(local_movies)


def get_details(movie_id, source='local'):
    """Get movie details from TMDB or local database."""
    if source == 'tmdb' and is_online():
        details = tmdb_service.get_movie_details(movie_id)
        if details:
            return details

    # Local database
    movie = movie_model.get_movie_by_id(movie_id)
    if movie:
        movie['source'] = 'local'
        movie['cast'] = movie.get('actors', [])
        movie['backdrop_path'] = ''
    return movie


def get_trending_movies():
    """Get trending movies - local popular."""
    # Always use local DB to ensure local images load quickly
    movies = movie_model.get_all_movies(limit=8)
    return _format_local_movies(movies)


def get_popular_movies():
    """Get popular movies - local."""
    # Always use local DB to ensure local images load quickly
    movies = movie_model.get_all_movies(limit=8)
    # Reverse or randomize slightly to differentiate from trending
    return _format_local_movies(movies[::-1])


def get_mood_movies(mood):
    """Get movies matching a mood."""
    genres = MOOD_GENRES.get(mood.lower(), [])
    results = []

    for genre in genres:
        if is_online():
            # Use local genre filtering even when online (AI feature)
            local = movie_model.get_movies_by_genre(genre)
            results.extend(_format_local_movies(local))
        else:
            local = movie_model.get_movies_by_genre(genre)
            results.extend(_format_local_movies(local))

    # Remove duplicates by title
    seen = set()
    unique = []
    for m in results:
        if m['title'] not in seen:
            seen.add(m['title'])
            unique.append(m)

    return unique[:8]


def _format_local_movies(movies):
    """Format local DB movies to match TMDB format."""
    formatted = []
    for m in movies:
        formatted.append({
            'id': m['id'],
            'title': m.get('title', ''),
            'overview': m.get('overview', ''),
            'poster_path': m.get('poster_path', ''),
            'release_date': m.get('release_date', ''),
            'rating': m.get('rating', 0),
            'genres': m.get('genres', []),
            'source': 'local'
        })
    return formatted
