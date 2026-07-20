# User behavior tracking operations
from models.db import execute_query, execute_update


def add_search_history(user_id, query):
    """Save a search query to history."""
    execute_update(
        "INSERT INTO search_history (user_id, query) VALUES (%s, %s)",
        (user_id, query)
    )


def get_search_history(user_id, limit=20):
    """Get recent search history for a user."""
    return execute_query(
        "SELECT * FROM search_history WHERE user_id = %s ORDER BY searched_at DESC LIMIT %s",
        (user_id, limit)
    )


def get_search_count():
    """Total number of searches."""
    result = execute_query("SELECT COUNT(*) as count FROM search_history")
    return result[0]['count'] if result else 0


def add_watch_history(user_id, movie_id):
    """Record that user watched/viewed a movie."""
    execute_update(
        "INSERT INTO watch_history (user_id, movie_id) VALUES (%s, %s)",
        (user_id, movie_id)
    )


def get_watch_history(user_id, limit=20):
    """Get recently watched movies for a user."""
    return execute_query("""
        SELECT m.*, wh.watched_at FROM watch_history wh
        JOIN movies m ON wh.movie_id = m.id
        WHERE wh.user_id = %s
        ORDER BY wh.watched_at DESC LIMIT %s
    """, (user_id, limit))


def add_favorite(user_id, movie_id):
    """Add a movie to favorites."""
    execute_update(
        "INSERT INTO favorites (user_id, movie_id) VALUES (%s, %s)",
        (user_id, movie_id)
    )


def remove_favorite(user_id, movie_id):
    """Remove a movie from favorites."""
    execute_update(
        "DELETE FROM favorites WHERE user_id = %s AND movie_id = %s",
        (user_id, movie_id)
    )


def get_favorites(user_id):
    """Get all favorite movies for a user."""
    return execute_query("""
        SELECT m.*, f.added_at FROM favorites f
        JOIN movies m ON f.movie_id = m.id
        WHERE f.user_id = %s
        ORDER BY f.added_at DESC
    """, (user_id,))


def is_favorite(user_id, movie_id):
    """Check if a movie is in user's favorites."""
    result = execute_query(
        "SELECT id FROM favorites WHERE user_id = %s AND movie_id = %s",
        (user_id, movie_id)
    )
    return len(result) > 0


def add_rating(user_id, movie_id, rating):
    """Add or update a movie rating."""
    existing = execute_query(
        "SELECT id FROM ratings WHERE user_id = %s AND movie_id = %s",
        (user_id, movie_id)
    )
    if existing:
        execute_update(
            "UPDATE ratings SET rating = %s WHERE user_id = %s AND movie_id = %s",
            (rating, user_id, movie_id)
        )
    else:
        execute_update(
            "INSERT INTO ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)",
            (user_id, movie_id, rating)
        )


def get_user_ratings(user_id):
    """Get all ratings by a user."""
    return execute_query("""
        SELECT r.*, m.title FROM ratings r
        JOIN movies m ON r.movie_id = m.id
        WHERE r.user_id = %s
        ORDER BY r.rated_at DESC
    """, (user_id,))


def get_user_preferences(user_id):
    """Get stored user preferences."""
    result = execute_query(
        "SELECT * FROM user_preferences WHERE user_id = %s", (user_id,)
    )
    return result[0] if result else None


def update_user_preferences(user_id, genres, actors, directors):
    """Update user AI preferences."""
    existing = get_user_preferences(user_id)
    if existing:
        execute_update("""
            UPDATE user_preferences SET preferred_genres=%s, preferred_actors=%s,
            preferred_directors=%s WHERE user_id=%s
        """, (genres, actors, directors, user_id))
    else:
        execute_update("""
            INSERT INTO user_preferences (user_id, preferred_genres, preferred_actors, preferred_directors)
            VALUES (%s, %s, %s, %s)
        """, (user_id, genres, actors, directors))


def get_user_stats():
    """Get total user count."""
    result = execute_query("SELECT COUNT(*) as count FROM users")
    return result[0]['count'] if result else 0
