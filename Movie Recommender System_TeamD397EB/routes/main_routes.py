# Main routes - Homepage, Movie Details, Search
from flask import Blueprint, render_template, request
from services import movie_service
from models import user_model
from ai.recommendation import RecommendationEngine

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage with trending, mood selector, and personalized recommendations."""
    user_id = 1

    # Get trending and popular movies
    trending = movie_service.get_trending_movies()
    popular = movie_service.get_popular_movies()

    # Get personalized recommendations if user has history
    engine = RecommendationEngine()
    personalized = []
    try:
        personalized = engine.get_personalized_homepage(user_id, n=8)
    except Exception:
        pass

    # Check online status
    online = movie_service.is_online()

    # Mood options
    moods = [
        {'name': 'happy', 'label': 'Happy', 'emoji': '😊'},
        {'name': 'sad', 'label': 'Sad', 'emoji': '😢'},
        {'name': 'funny', 'label': 'Funny', 'emoji': '😂'},
        {'name': 'romantic', 'label': 'Romantic', 'emoji': '💕'},
        {'name': 'thriller', 'label': 'Thriller', 'emoji': '😰'},
        {'name': 'horror', 'label': 'Horror', 'emoji': '👻'},
        {'name': 'adventure', 'label': 'Adventure', 'emoji': '🗺️'},
        {'name': 'family', 'label': 'Family', 'emoji': '👨‍👩‍👧‍👦'},
        {'name': 'mystery', 'label': 'Mystery', 'emoji': '🔍'},
        {'name': 'scifi', 'label': 'Sci-Fi', 'emoji': '🚀'},
    ]

    return render_template('index.html',
                           trending=trending,
                           popular=popular,
                           personalized=personalized,
                           moods=moods,
                           online=online)


@main_bp.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Movie details page with recommendations."""
    user_id = 1
    source = request.args.get('source', 'local')

    # Get movie details
    movie = movie_service.get_details(movie_id, source)
    if not movie:
        return render_template('search_results.html', query='', results=[], error='Movie not found')

    # Track watch history (only for local movies)
    if source == 'local':
        try:
            user_model.add_watch_history(user_id, movie_id)
        except Exception:
            pass

    # Check if favorite
    is_fav = False
    if source == 'local':
        is_fav = user_model.is_favorite(user_id, movie_id)

    # Get AI recommendations (for local movies)
    recommendations = []
    if source == 'local':
        try:
            engine = RecommendationEngine()
            recommendations = engine.get_hybrid_recommendations(user_id, movie_id, n=8)
        except Exception:
            pass

    # If no AI recommendations, try TMDB recommendations
    if not recommendations and source == 'tmdb' and movie_service.is_online():
        from services import tmdb_service
        recommendations = tmdb_service.get_tmdb_recommendations(movie_id)

    return render_template('movie_detail.html',
                           movie=movie,
                           recommendations=recommendations,
                           is_favorite=is_fav,
                           source=source)


@main_bp.route('/search')
def search_results():
    """Search results page."""
    query = request.args.get('q', '').strip()
    year = request.args.get('year', '').strip()
    if not query:
        return render_template('search_results.html', query='', results=[])

    results = movie_service.search(query, user_id=1, year=year)
    return render_template('search_results.html', query=query, results=results)
