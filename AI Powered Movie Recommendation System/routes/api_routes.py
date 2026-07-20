# API routes - AJAX endpoints for search, favorites, ratings, mood
from flask import Blueprint, request, jsonify
from services import movie_service, search_service
from models import movie_model, user_model

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/search')
def api_search():
    """Autocomplete search suggestions."""
    query = request.args.get('q', '').strip()
    year = request.args.get('year', '').strip()
    if not query:
        return jsonify([])

    # Get all local movie titles for fuzzy matching
    all_movies = movie_model.get_all_movie_titles()
    if year:
        all_movies = [m for m in all_movies if m.get('release_date') and m['release_date'].startswith(year)]

    titles = [m['title'] for m in all_movies]

    # Fuzzy autocomplete
    suggestions = search_service.get_autocomplete(query, titles, limit=5)

    # Add movie IDs to suggestions
    results = []
    for s in suggestions:
        for m in all_movies:
            if m['title'] == s['title']:
                results.append({
                    'id': m['id'],
                    'title': m['title'],
                    'rating': m.get('rating', 0),
                    'poster_path': m.get('poster_path', ''),
                    'source': 'local',
                    'score': s['score']
                })
                break
    return jsonify(results)


@api_bp.route('/api/favorite', methods=['POST'])
def toggle_favorite():
    """Toggle a movie as favorite."""
    data = request.get_json()
    movie_id = data.get('movie_id')
    user_id = 1

    if not movie_id:
        return jsonify({'status': 'error', 'message': 'Movie ID required'})

    if user_model.is_favorite(user_id, movie_id):
        user_model.remove_favorite(user_id, movie_id)
        return jsonify({'status': 'ok', 'is_favorite': False})
    else:
        user_model.add_favorite(user_id, movie_id)
        return jsonify({'status': 'ok', 'is_favorite': True})


@api_bp.route('/api/rate', methods=['POST'])
def rate_movie():
    """Rate a movie."""
    data = request.get_json()
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    user_id = 1

    if not movie_id or rating is None:
        return jsonify({'status': 'error', 'message': 'Movie ID and rating required'})

    user_model.add_rating(user_id, movie_id, float(rating))
    return jsonify({'status': 'ok'})


@api_bp.route('/api/mood/<mood>')
def mood_movies(mood):
    """Get movies matching a mood."""
    movies = movie_service.get_mood_movies(mood)
    return jsonify(movies)


@api_bp.route('/api/recommendations/<int:movie_id>')
def get_recommendations(movie_id):
    """Get AI recommendations for a movie."""
    from ai.recommendation import RecommendationEngine
    engine = RecommendationEngine()
    try:
        recs = engine.get_hybrid_recommendations(1, movie_id, n=8)
        # Clean for JSON
        clean = []
        for r in recs:
            clean.append({
                'id': r.get('id'),
                'title': r.get('title', ''),
                'poster_path': r.get('poster_path', ''),
                'rating': r.get('rating', 0),
                'hybrid_score': r.get('hybrid_score', 0),
                'explanation': r.get('explanation', []),
                'source': 'local'
            })
        return jsonify(clean)
    except Exception as e:
        return jsonify([])


@api_bp.route('/api/status')
def api_status():
    """Check online/offline status."""
    return jsonify({'online': movie_service.is_online()})


@api_bp.route('/api/watch', methods=['POST'])
def track_watch():
    """Track that a user viewed a movie."""
    data = request.get_json()
    movie_id = data.get('movie_id')
    if movie_id:
        user_model.add_watch_history(1, movie_id)
    return jsonify({'status': 'ok'})
