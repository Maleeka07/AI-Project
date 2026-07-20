# Smart search service with fuzzy matching
from rapidfuzz import fuzz, process


def smart_search(query, movie_titles, limit=10):
    """Fuzzy search against a list of movie titles. Returns sorted matches."""
    if not query or not movie_titles:
        return []
    results = process.extract(query, movie_titles, scorer=fuzz.WRatio, limit=limit)
    # results = [(match_string, score, index), ...]
    return [{'title': r[0], 'score': r[1], 'index': r[2]} for r in results if r[1] > 50]


def correct_typo(query, movie_titles):
    """Try to correct a typo in the search query."""
    if not query or not movie_titles:
        return query
    best = process.extractOne(query, movie_titles, scorer=fuzz.WRatio)
    if best and best[1] > 70:
        return best[0]
    return query


def get_autocomplete(query, movie_titles, limit=5):
    """Get autocomplete suggestions for a partial query."""
    if not query or not movie_titles:
        return []
    results = process.extract(query, movie_titles, scorer=fuzz.WRatio, limit=limit)
    return [{'title': r[0], 'score': r[1]} for r in results if r[1] > 40]
