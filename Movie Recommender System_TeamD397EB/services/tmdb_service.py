# TMDB API wrapper service
import requests
from config import Config

API_KEY = Config.TMDB_API_KEY
BASE_URL = Config.TMDB_BASE_URL
IMG_URL = Config.TMDB_IMAGE_URL


def check_internet():
    """Check if TMDB API is reachable."""
    try:
        r = requests.get(f"{BASE_URL}/configuration", params={'api_key': API_KEY}, timeout=1)
        return r.status_code == 200
    except Exception:
        return False


def search_movies(query):
    """Search movies on TMDB."""
    try:
        r = requests.get(f"{BASE_URL}/search/movie", params={
            'api_key': API_KEY, 'query': query
        }, timeout=5)
        data = r.json()
        results = []
        for m in data.get('results', [])[:12]:
            results.append({
                'id': m['id'],
                'title': m.get('title', ''),
                'overview': m.get('overview', ''),
                'poster_path': f"{IMG_URL}{m['poster_path']}" if m.get('poster_path') else '',
                'release_date': m.get('release_date', ''),
                'rating': round(m.get('vote_average', 0), 1),
                'source': 'tmdb'
            })
        return results
    except Exception:
        return []


def get_movie_details(tmdb_id):
    """Get full movie details from TMDB."""
    try:
        r = requests.get(f"{BASE_URL}/movie/{tmdb_id}", params={
            'api_key': API_KEY, 'append_to_response': 'credits,videos'
        }, timeout=5)
        m = r.json()

        # Extract director
        director = ''
        for crew in m.get('credits', {}).get('crew', []):
            if crew.get('job') == 'Director':
                director = crew['name']
                break

        # Extract cast (top 10)
        cast = [c['name'] for c in m.get('credits', {}).get('cast', [])[:10]]

        # Extract trailer
        trailer = ''
        for video in m.get('videos', {}).get('results', []):
            if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                trailer = f"https://www.youtube.com/watch?v={video['key']}"
                break

        # Extract genres
        genres = [g['name'] for g in m.get('genres', [])]

        # Production company
        companies = m.get('production_companies', [])
        production = companies[0]['name'] if companies else ''

        return {
            'id': m['id'],
            'title': m.get('title', ''),
            'overview': m.get('overview', ''),
            'poster_path': f"{IMG_URL}{m['poster_path']}" if m.get('poster_path') else '',
            'backdrop_path': f"https://image.tmdb.org/t/p/original{m['backdrop_path']}" if m.get('backdrop_path') else '',
            'release_date': m.get('release_date', ''),
            'runtime': m.get('runtime', 0),
            'rating': round(m.get('vote_average', 0), 1),
            'language': m.get('original_language', 'en'),
            'director': director,
            'cast': cast,
            'genres': genres,
            'trailer_link': trailer,
            'production_company': production,
            'popularity': m.get('popularity', 0),
            'source': 'tmdb'
        }
    except Exception:
        return None


def get_trending():
    """Get trending movies from TMDB."""
    try:
        r = requests.get(f"{BASE_URL}/trending/movie/week", params={
            'api_key': API_KEY
        }, timeout=5)
        data = r.json()
        results = []
        for m in data.get('results', [])[:8]:
            results.append({
                'id': m['id'],
                'title': m.get('title', ''),
                'poster_path': f"{IMG_URL}{m['poster_path']}" if m.get('poster_path') else '',
                'release_date': m.get('release_date', ''),
                'rating': round(m.get('vote_average', 0), 1),
                'source': 'tmdb'
            })
        return results
    except Exception:
        return []


def get_popular():
    """Get popular movies from TMDB."""
    try:
        r = requests.get(f"{BASE_URL}/movie/popular", params={
            'api_key': API_KEY
        }, timeout=5)
        data = r.json()
        results = []
        for m in data.get('results', [])[:8]:
            results.append({
                'id': m['id'],
                'title': m.get('title', ''),
                'poster_path': f"{IMG_URL}{m['poster_path']}" if m.get('poster_path') else '',
                'release_date': m.get('release_date', ''),
                'rating': round(m.get('vote_average', 0), 1),
                'source': 'tmdb'
            })
        return results
    except Exception:
        return []


def get_tmdb_recommendations(tmdb_id):
    """Get TMDB's own recommendations for a movie."""
    try:
        r = requests.get(f"{BASE_URL}/movie/{tmdb_id}/recommendations", params={
            'api_key': API_KEY
        }, timeout=5)
        data = r.json()
        results = []
        for m in data.get('results', [])[:8]:
            results.append({
                'id': m['id'],
                'title': m.get('title', ''),
                'poster_path': f"{IMG_URL}{m['poster_path']}" if m.get('poster_path') else '',
                'release_date': m.get('release_date', ''),
                'rating': round(m.get('vote_average', 0), 1),
                'source': 'tmdb'
            })
        return results
    except Exception:
        return []
