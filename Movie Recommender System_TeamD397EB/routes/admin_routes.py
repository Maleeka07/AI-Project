# Admin panel routes
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response
from models import movie_model, user_model
import json

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
def dashboard():
    """Admin dashboard with statistics."""
    stats = {
        'movies': movie_model.get_movie_count(),
        'users': user_model.get_user_stats(),
        'searches': user_model.get_search_count()
    }
    return render_template('admin/dashboard.html', stats=stats)


@admin_bp.route('/admin/movies')
def movies_list():
    """List all movies."""
    movies = movie_model.get_all_movies(limit=100)
    return render_template('admin/movies.html', movies=movies)


@admin_bp.route('/admin/movies/add', methods=['GET', 'POST'])
def add_movie():
    """Add a new movie."""
    if request.method == 'POST':
        data = {
            'title': request.form.get('title', ''),
            'overview': request.form.get('overview', ''),
            'release_date': request.form.get('release_date', ''),
            'runtime': int(request.form.get('runtime', 0) or 0),
            'rating': float(request.form.get('rating', 0) or 0),
            'language': request.form.get('language', 'en'),
            'poster_path': request.form.get('poster_path', ''),
            'trailer_link': request.form.get('trailer_link', ''),
            'keywords': request.form.get('keywords', ''),
            'popularity': float(request.form.get('popularity', 0) or 0),
            'director': request.form.get('director', ''),
            'production_company': request.form.get('production_company', ''),
            'genres': request.form.get('genres', ''),
            'cast': request.form.get('cast', ''),
        }
        movie_model.add_movie(data)
        flash('Movie added successfully!', 'success')
        return redirect(url_for('admin.movies_list'))

    genres = movie_model.get_all_genres()
    return render_template('admin/add_movie.html', movie=None, genres=genres)


@admin_bp.route('/admin/movies/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    """Edit an existing movie."""
    movie = movie_model.get_movie_by_id(movie_id)
    if not movie:
        flash('Movie not found!', 'error')
        return redirect(url_for('admin.movies_list'))

    if request.method == 'POST':
        data = {
            'title': request.form.get('title', ''),
            'overview': request.form.get('overview', ''),
            'release_date': request.form.get('release_date', ''),
            'runtime': int(request.form.get('runtime', 0) or 0),
            'rating': float(request.form.get('rating', 0) or 0),
            'language': request.form.get('language', 'en'),
            'poster_path': request.form.get('poster_path', ''),
            'trailer_link': request.form.get('trailer_link', ''),
            'keywords': request.form.get('keywords', ''),
            'popularity': float(request.form.get('popularity', 0) or 0),
            'director': request.form.get('director', ''),
            'production_company': request.form.get('production_company', ''),
            'genres': request.form.get('genres', ''),
            'cast': request.form.get('cast', ''),
        }
        movie_model.update_movie(movie_id, data)
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('admin.movies_list'))

    # Prepare data for form
    movie['genres_str'] = ', '.join(movie.get('genres', []))
    movie['cast_str'] = ', '.join(movie.get('actors', []))
    genres = movie_model.get_all_genres()
    return render_template('admin/add_movie.html', movie=movie, genres=genres)


@admin_bp.route('/admin/movies/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """Delete a movie."""
    movie_model.delete_movie(movie_id)
    flash('Movie deleted.', 'success')
    return redirect(url_for('admin.movies_list'))


@admin_bp.route('/admin/export')
def export_database():
    """Export all movies as JSON."""
    movies = movie_model.get_all_movies(limit=100)
    # Convert datetime objects to strings
    for m in movies:
        for key, val in m.items():
            if hasattr(val, 'isoformat'):
                m[key] = val.isoformat()

    data = json.dumps(movies, indent=2, default=str)
    return Response(
        data,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment; filename=movies_export.json'}
    )
