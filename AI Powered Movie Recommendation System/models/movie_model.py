# Movie database operations — OPTIMIZED (no N+1 queries)
from models.db import execute_query, execute_update


def get_all_movies(limit=None):
    """Get movies with genres using a single JOIN query (no N+1)."""
    query = """
        SELECT m.*, GROUP_CONCAT(DISTINCT g.name SEPARATOR ', ') as genre_list
        FROM movies m
        LEFT JOIN movie_genres mg ON m.id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.id
        GROUP BY m.id
        ORDER BY m.popularity DESC
    """
    if limit:
        query += f" LIMIT {limit}"

    movies = execute_query(query)
    for movie in movies:
        movie['genres'] = [g.strip() for g in (movie.get('genre_list') or '').split(',') if g.strip()]
        del movie['genre_list']
    return movies


def get_all_movie_titles():
    """Get only basic movie info for autocomplete (fast)."""
    return execute_query("SELECT id, title, release_date FROM movies")


def get_movie_by_id(movie_id):
    """Get a single movie with all details."""
    movies = execute_query("SELECT * FROM movies WHERE id = %s", (movie_id,))
    if not movies:
        return None
    movie = movies[0]
    movie['genres'] = _get_movie_genres(movie_id)
    movie['actors'] = _get_movie_actors(movie_id)
    return movie


def search_movies_local(query, year=''):
    """Search movies by title (local database) — optimized with JOIN."""
    sql = """
        SELECT m.*, GROUP_CONCAT(DISTINCT g.name SEPARATOR ', ') as genre_list
        FROM movies m
        LEFT JOIN movie_genres mg ON m.id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.id
        WHERE m.title LIKE %s
    """
    params = [f"%{query}%"]

    if year:
        sql += " AND m.release_date LIKE %s"
        params.append(f"{year}%")

    sql += " GROUP BY m.id ORDER BY m.popularity DESC LIMIT 50"

    movies = execute_query(sql, tuple(params))
    for movie in movies:
        movie['genres'] = [g.strip() for g in (movie.get('genre_list') or '').split(',') if g.strip()]
        del movie['genre_list']
    return movies


def get_movies_by_genre(genre_name):
    """Get movies filtered by genre name — optimized."""
    movies = execute_query("""
        SELECT m.*, GROUP_CONCAT(DISTINCT g2.name SEPARATOR ', ') as genre_list
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.id
        LEFT JOIN movie_genres mg2 ON m.id = mg2.movie_id
        LEFT JOIN genres g2 ON mg2.genre_id = g2.id
        WHERE g.name = %s
        GROUP BY m.id
        ORDER BY m.popularity DESC
        LIMIT 20
    """, (genre_name,))
    for movie in movies:
        movie['genres'] = [g.strip() for g in (movie.get('genre_list') or '').split(',') if g.strip()]
        del movie['genre_list']
    return movies


def add_movie(data):
    """Insert a new movie into the database."""
    movie_id = execute_update("""
        INSERT INTO movies (title, overview, release_date, runtime, rating, language,
            poster_path, trailer_link, keywords, popularity, director, production_company)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get('title', ''), data.get('overview', ''),
        data.get('release_date', ''), data.get('runtime', 0),
        data.get('rating', 0), data.get('language', 'en'),
        data.get('poster_path', ''), data.get('trailer_link', ''),
        data.get('keywords', ''), data.get('popularity', 0),
        data.get('director', ''), data.get('production_company', '')
    ))

    # Link genres
    if data.get('genres'):
        _link_genres(movie_id, data['genres'])

    # Link actors
    if data.get('cast'):
        _link_actors(movie_id, data['cast'])

    return movie_id


def update_movie(movie_id, data):
    """Update an existing movie."""
    execute_update("""
        UPDATE movies SET title=%s, overview=%s, release_date=%s, runtime=%s,
            rating=%s, language=%s, poster_path=%s, trailer_link=%s,
            keywords=%s, popularity=%s, director=%s, production_company=%s
        WHERE id=%s
    """, (
        data.get('title', ''), data.get('overview', ''),
        data.get('release_date', ''), data.get('runtime', 0),
        data.get('rating', 0), data.get('language', 'en'),
        data.get('poster_path', ''), data.get('trailer_link', ''),
        data.get('keywords', ''), data.get('popularity', 0),
        data.get('director', ''), data.get('production_company', ''),
        movie_id
    ))

    # Re-link genres
    if data.get('genres'):
        execute_update("DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))
        _link_genres(movie_id, data['genres'])

    # Re-link actors
    if data.get('cast'):
        execute_update("DELETE FROM movie_actors WHERE movie_id = %s", (movie_id,))
        _link_actors(movie_id, data['cast'])


def delete_movie(movie_id):
    """Delete a movie."""
    execute_update("DELETE FROM movies WHERE id = %s", (movie_id,))


def get_movie_count():
    """Get total number of movies."""
    result = execute_query("SELECT COUNT(*) as count FROM movies")
    return result[0]['count'] if result else 0


def get_movies_with_features():
    """Get movies with combined text features for AI — OPTIMIZED single query."""
    movies = execute_query("""
        SELECT m.*,
            GROUP_CONCAT(DISTINCT g.name SEPARATOR ' ') as genres_text,
            GROUP_CONCAT(DISTINCT a.name SEPARATOR ' ') as actors_text
        FROM movies m
        LEFT JOIN movie_genres mg ON m.id = mg.movie_id
        LEFT JOIN genres g ON mg.genre_id = g.id
        LEFT JOIN movie_actors ma ON m.id = ma.movie_id
        LEFT JOIN actors a ON ma.actor_id = a.id
        GROUP BY m.id
        ORDER BY m.id
    """)
    for movie in movies:
        genres_text = movie.get('genres_text') or ''
        actors_text = movie.get('actors_text') or ''
        movie['genres'] = [g.strip() for g in genres_text.split(' ') if g.strip()] if genres_text else []
        movie['actors'] = [a.strip() for a in actors_text.split(' ') if a.strip()] if actors_text else []
        keywords = movie.get('keywords', '') or ''
        overview = movie.get('overview', '') or ''
        director = movie.get('director', '') or ''
        movie['features'] = f"{genres_text} {keywords} {overview} {actors_text} {director}"
    return movies


def get_all_genres():
    """Get all genre names."""
    return execute_query("SELECT * FROM genres ORDER BY name")


def _get_movie_genres(movie_id):
    """Get genre names for a movie."""
    rows = execute_query("""
        SELECT g.name FROM genres g
        JOIN movie_genres mg ON g.id = mg.genre_id
        WHERE mg.movie_id = %s
    """, (movie_id,))
    return [r['name'] for r in rows]


def _get_movie_actors(movie_id):
    """Get actor names for a movie."""
    rows = execute_query("""
        SELECT a.name FROM actors a
        JOIN movie_actors ma ON a.id = ma.actor_id
        WHERE ma.movie_id = %s
    """, (movie_id,))
    return [r['name'] for r in rows]


def _link_genres(movie_id, genres_str):
    """Link genres to a movie (comma-separated string)."""
    for genre_name in genres_str.split(','):
        genre_name = genre_name.strip()
        if not genre_name:
            continue
        # Find or create genre
        existing = execute_query("SELECT id FROM genres WHERE name = %s", (genre_name,))
        if existing:
            genre_id = existing[0]['id']
        else:
            genre_id = execute_update("INSERT INTO genres (name) VALUES (%s)", (genre_name,))
        execute_update(
            "INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)",
            (movie_id, genre_id)
        )


def _link_actors(movie_id, cast_str):
    """Link actors to a movie (comma-separated string)."""
    for actor_name in cast_str.split(','):
        actor_name = actor_name.strip()
        if not actor_name:
            continue
        existing = execute_query("SELECT id FROM actors WHERE name = %s", (actor_name,))
        if existing:
            actor_id = existing[0]['id']
        else:
            actor_id = execute_update("INSERT INTO actors (name) VALUES (%s)", (actor_name,))
        execute_update(
            "INSERT IGNORE INTO movie_actors (movie_id, actor_id) VALUES (%s, %s)",
            (movie_id, actor_id)
        )
