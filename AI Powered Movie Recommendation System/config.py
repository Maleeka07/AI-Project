# Configuration for AI-Powered Movie Recommendation Feed

class Config:
    SECRET_KEY = 'movie-rec-secret-key-2024'

    # MySQL Database (XAMPP default)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DATABASE = 'movie_recommendation_db'

    # TMDB API - Get your free key from https://www.themoviedb.org/settings/api
    TMDB_API_KEY = 'YOUR_TMDB_API_KEY_HERE'
    TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_URL = 'https://image.tmdb.org/t/p/w500'
