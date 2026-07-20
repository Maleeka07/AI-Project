# AI Recommendation Engine — OPTIMIZED with caching
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import movie_model
from ai.user_profile import UserProfile
import time

# Global cache so we don't rebuild TF-IDF on every request
_model_cache = {'movies': None, 'matrix': None, 'vectorizer': None, 'time': 0}
CACHE_TTL = 300  # 5 minutes


class RecommendationEngine:
    """Content-based recommendation engine with hybrid scoring."""

    def __init__(self):
        self._tfidf_matrix = None
        self._movies = None
        self._vectorizer = None

    def _build_model(self):
        """Build TF-IDF model — uses cache to avoid rebuilding every request."""
        now = time.time()

        # Use cached model if available and fresh
        if _model_cache['movies'] and (now - _model_cache['time']) < CACHE_TTL:
            self._movies = _model_cache['movies']
            self._tfidf_matrix = _model_cache['matrix']
            self._vectorizer = _model_cache['vectorizer']
            return

        self._movies = movie_model.get_movies_with_features()
        if not self._movies:
            return

        features = [m.get('features', '') for m in self._movies]

        self._vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self._tfidf_matrix = self._vectorizer.fit_transform(features)

        # Save to cache
        _model_cache['movies'] = self._movies
        _model_cache['matrix'] = self._tfidf_matrix
        _model_cache['vectorizer'] = self._vectorizer
        _model_cache['time'] = now

    def get_similar_movies(self, movie_id, n=8):
        """Get n most similar movies using cosine similarity."""
        self._build_model()
        if self._tfidf_matrix is None or not self._movies:
            return []

        movie_idx = None
        for i, m in enumerate(self._movies):
            if m['id'] == movie_id:
                movie_idx = i
                break

        if movie_idx is None:
            return []

        sim_scores = cosine_similarity(
            self._tfidf_matrix[movie_idx:movie_idx + 1],
            self._tfidf_matrix
        ).flatten()

        similar_indices = sim_scores.argsort()[::-1][1:n + 1]

        results = []
        for idx in similar_indices:
            movie = self._movies[idx].copy()
            movie['similarity'] = round(float(sim_scores[idx]) * 100, 1)
            movie['source'] = 'local'
            results.append(movie)

        return results

    def get_hybrid_recommendations(self, user_id, movie_id, n=8):
        """Hybrid scoring: 40% behavior + 30% similarity + 20% genre + 10% popularity."""
        self._build_model()
        if self._tfidf_matrix is None or not self._movies:
            return []

        profile = UserProfile(user_id)
        profile.build_profile()

        movie_idx = None
        target_movie = None
        for i, m in enumerate(self._movies):
            if m['id'] == movie_id:
                movie_idx = i
                target_movie = m
                break

        if movie_idx is None:
            return self.get_similar_movies(movie_id, n)

        sim_scores = cosine_similarity(
            self._tfidf_matrix[movie_idx:movie_idx + 1],
            self._tfidf_matrix
        ).flatten()

        scored_movies = []
        max_popularity = max((m.get('popularity', 1) for m in self._movies), default=1)

        for i, movie in enumerate(self._movies):
            if movie['id'] == movie_id:
                continue

            similarity_score = float(sim_scores[i])
            behavior_score = profile.get_behavior_score(movie)

            target_genres = set(target_movie.get('genres', []))
            movie_genres = set(movie.get('genres', []))
            genre_overlap = len(target_genres & movie_genres)
            genre_total = max(len(target_genres | movie_genres), 1)
            genre_score = genre_overlap / genre_total

            pop_score = float(movie.get('popularity', 0)) / max(max_popularity, 1)

            hybrid = (0.4 * behavior_score) + (0.3 * similarity_score) + (0.2 * genre_score) + (0.1 * pop_score)

            movie_copy = movie.copy()
            movie_copy['hybrid_score'] = round(hybrid * 100, 1)
            movie_copy['similarity'] = round(similarity_score * 100, 1)
            movie_copy['explanation'] = self.get_explanation(movie, target_movie, profile, similarity_score)
            movie_copy['source'] = 'local'
            scored_movies.append(movie_copy)

        scored_movies.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return scored_movies[:n]

    def get_explanation(self, movie, target_movie, profile, similarity_score):
        """Generate explainable AI reasons for a recommendation."""
        reasons = []

        target_genres = set(target_movie.get('genres', []))
        movie_genres = set(movie.get('genres', []))
        common_genres = target_genres & movie_genres
        if common_genres:
            reasons.append(f"✓ Same Genre: {', '.join(list(common_genres)[:2])}")

        if similarity_score > 0.3:
            reasons.append("✓ Similar Story")

        if movie.get('director') and movie['director'] == target_movie.get('director'):
            reasons.append(f"✓ Same Director: {movie['director']}")

        target_cast = set(target_movie.get('actors', []))
        movie_cast = set(movie.get('actors', []))
        common_cast = target_cast & movie_cast
        if common_cast:
            reasons.append(f"✓ Similar Cast: {', '.join(list(common_cast)[:2])}")

        if target_movie.get('title'):
            reasons.append(f"✓ You viewed {target_movie['title']}")

        match_pct = round(similarity_score * 100)
        reasons.append(f"✓ {match_pct}% Match")

        return reasons

    def get_personalized_homepage(self, user_id, n=8):
        """Get personalized recommendations for homepage."""
        self._build_model()
        if self._tfidf_matrix is None or not self._movies:
            return []

        profile = UserProfile(user_id)
        profile.build_profile()

        # If user has no history, return popular movies
        if not profile.top_genres and not profile.top_actors:
            return sorted(self._movies, key=lambda x: x.get('popularity', 0), reverse=True)[:n]

        scored = []
        for movie in self._movies:
            score = profile.get_behavior_score(movie)
            movie_copy = movie.copy()
            movie_copy['hybrid_score'] = round(score * 100, 1)
            movie_copy['source'] = 'local'
            scored.append(movie_copy)

        scored.sort(key=lambda x: x['hybrid_score'], reverse=True)
        return scored[:n]
