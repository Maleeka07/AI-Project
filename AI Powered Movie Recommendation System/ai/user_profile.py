# User AI Profile - analyzes behavior to build evolving preferences
from models import user_model, movie_model


class UserProfile:
    """Builds and maintains an evolving AI profile for a user."""

    def __init__(self, user_id):
        self.user_id = user_id
        self.top_genres = []
        self.top_actors = []
        self.top_directors = []
        self.avg_rating = 0.0
        self._genre_scores = {}

    def build_profile(self):
        """Analyze user history and build their AI profile."""
        # Get user data
        watch_history = user_model.get_watch_history(self.user_id)
        favorites = user_model.get_favorites(self.user_id)
        ratings = user_model.get_user_ratings(self.user_id)

        genre_count = {}
        actor_count = {}
        director_count = {}
        total_rating = 0.0
        rating_count = 0

        # Analyze watched movies
        for entry in watch_history:
            movie = movie_model.get_movie_by_id(entry.get('id') or entry.get('movie_id'))
            if movie:
                self._count_features(movie, genre_count, actor_count, director_count, weight=1)

        # Analyze favorites (higher weight)
        for entry in favorites:
            movie = movie_model.get_movie_by_id(entry.get('id') or entry.get('movie_id'))
            if movie:
                self._count_features(movie, genre_count, actor_count, director_count, weight=2)

        # Analyze ratings
        for r in ratings:
            total_rating += float(r.get('rating', 0))
            rating_count += 1

        # Compute averages and top preferences
        self.top_genres = sorted(genre_count, key=genre_count.get, reverse=True)[:5]
        self.top_actors = sorted(actor_count, key=actor_count.get, reverse=True)[:5]
        self.top_directors = sorted(director_count, key=director_count.get, reverse=True)[:3]
        self.avg_rating = round(total_rating / max(rating_count, 1), 1)
        self._genre_scores = genre_count

        # Save to database
        self._save_preferences()

    def _count_features(self, movie, genre_count, actor_count, director_count, weight=1):
        """Count genre/actor/director occurrences from a movie."""
        for genre in movie.get('genres', []):
            genre_count[genre] = genre_count.get(genre, 0) + weight

        for actor in movie.get('actors', []):
            actor_count[actor] = actor_count.get(actor, 0) + weight

        director = movie.get('director', '')
        if director:
            director_count[director] = director_count.get(director, 0) + weight

    def get_genre_scores(self):
        """Get genre preference scores."""
        return self._genre_scores

    def get_behavior_score(self, movie):
        """Score a movie 0-1 based on how well it matches user preferences."""
        if not self.top_genres and not self.top_actors:
            return 0.0

        score = 0.0
        max_score = 0.0

        # Genre match (60% weight)
        movie_genres = set(movie.get('genres', []))
        user_genres = set(self.top_genres)
        if user_genres:
            genre_overlap = len(movie_genres & user_genres)
            score += 0.6 * (genre_overlap / max(len(user_genres), 1))
            max_score += 0.6

        # Actor match (25% weight)
        movie_actors = set(movie.get('actors', []))
        user_actors = set(self.top_actors)
        if user_actors:
            actor_overlap = len(movie_actors & user_actors)
            score += 0.25 * (actor_overlap / max(len(user_actors), 1))
            max_score += 0.25

        # Director match (15% weight)
        movie_director = movie.get('director', '')
        if self.top_directors and movie_director in self.top_directors:
            score += 0.15
        max_score += 0.15

        return score / max(max_score, 0.01)

    def _save_preferences(self):
        """Save computed preferences to database."""
        user_model.update_user_preferences(
            self.user_id,
            ','.join(self.top_genres),
            ','.join(self.top_actors),
            ','.join(self.top_directors)
        )
