// AI-Powered Movie Recommendation Feed - Main JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // =================== SEARCH AUTOCOMPLETE ===================
    const searchInput = document.getElementById('searchInput');
    const dropdown = document.getElementById('autocompleteDropdown');
    let debounceTimer;

    if (searchInput && dropdown) {
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const query = this.value.trim();

            if (query.length < 2) {
                dropdown.classList.remove('show');
                dropdown.innerHTML = '';
                return;
            }

            debounceTimer = setTimeout(function () {
                var year = '';
                var searchYear = document.getElementById('searchYear');
                if (searchYear) {
                    year = searchYear.value;
                }
                var url = '/api/search?q=' + encodeURIComponent(query);
                if (year) {
                    url += '&year=' + encodeURIComponent(year);
                }
                fetch(url)
                    .then(function (res) { return res.json(); })
                    .then(function (data) {
                        if (data.length === 0) {
                            dropdown.classList.remove('show');
                            return;
                        }
                        dropdown.innerHTML = '';
                        data.forEach(function (movie) {
                            var item = document.createElement('div');
                            item.className = 'autocomplete-item';
                            item.innerHTML = '<span>🎬 ' + movie.title + '</span><span class="ac-rating">⭐ ' + movie.rating + '</span>';
                            item.addEventListener('click', function () {
                                window.location.href = '/movie/' + movie.id + '?source=' + movie.source;
                            });
                            dropdown.appendChild(item);
                        });
                        dropdown.classList.add('show');
                    })
                    .catch(function () {
                        dropdown.classList.remove('show');
                    });
            }, 300);
        });

        // Hide dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });
    }

    // =================== ONLINE STATUS CHECK ===================
    function checkStatus() {
        fetch('/api/status')
            .then(function (res) { return res.json(); })
            .then(function (data) {
                var dot = document.getElementById('statusDot');
                if (dot) {
                    if (data.online) {
                        dot.classList.add('online');
                        dot.title = 'Online - TMDB Connected';
                    } else {
                        dot.classList.remove('online');
                        dot.title = 'Offline - Using Local Database';
                    }
                }
            })
            .catch(function () { });
    }

    checkStatus();

    // Auto-close flash messages after 5 seconds
    var flashes = document.querySelectorAll('.flash-message');
    flashes.forEach(function (flash) {
        setTimeout(function () { flash.remove(); }, 5000);
    });
});


// =================== FAVORITE TOGGLE ===================
function toggleFavorite(movieId) {
    fetch('/api/favorite', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie_id: movieId })
    })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            var btn = document.getElementById('favBtn');
            var icon = document.getElementById('favIcon');
            if (data.is_favorite) {
                btn.classList.add('active');
                icon.textContent = '❤️';
                showToast('Added to favorites!');
            } else {
                btn.classList.remove('active');
                icon.textContent = '🤍';
                showToast('Removed from favorites');
            }
        })
        .catch(function () {
            showToast('Error updating favorite', 'error');
        });
}


// =================== RATE MOVIE ===================
function rateMovie(movieId, rating) {
    fetch('/api/rate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie_id: movieId, rating: rating })
    })
        .then(function (res) { return res.json(); })
        .then(function () {
            // Highlight stars
            var stars = document.querySelectorAll('#starRating .star');
            stars.forEach(function (star) {
                var val = parseInt(star.getAttribute('data-value'));
                if (val <= rating) {
                    star.textContent = '★';
                    star.classList.add('filled');
                } else {
                    star.textContent = '☆';
                    star.classList.remove('filled');
                }
            });
            showToast('Rated ' + rating + '/10!');
        })
        .catch(function () {
            showToast('Error saving rating', 'error');
        });
}


// =================== MOOD MOVIES ===================
function loadMoodMovies(mood) {
    // Highlight active button
    var buttons = document.querySelectorAll('.mood-btn');
    buttons.forEach(function (btn) { btn.classList.remove('active'); });
    var activeBtn = document.querySelector('[data-mood="' + mood + '"]');
    if (activeBtn) activeBtn.classList.add('active');

    var container = document.getElementById('moodResults');
    if (!container) return;

    container.innerHTML = '<p style="text-align:center; color:#9CA3AF;">Loading...</p>';

    fetch('/api/mood/' + mood)
        .then(function (res) { return res.json(); })
        .then(function (movies) {
            if (movies.length === 0) {
                container.innerHTML = '<p style="text-align:center; color:#9CA3AF;">No movies found for this mood.</p>';
                return;
            }
            var html = '';
            movies.forEach(function (movie) {
                var posterUrl = movie.poster_path;
                if (posterUrl && !posterUrl.startsWith('http')) {
                    posterUrl = '/static/' + posterUrl.replace('static/', '').replace('/static/', '');
                }
                var poster = posterUrl
                    ? '<img src="' + posterUrl + '" alt="' + movie.title + '" loading="lazy">'
                    : '<div class="poster-placeholder">🎬</div>';
                var year = movie.release_date ? movie.release_date.substring(0, 4) : '';

                html += '<a href="/movie/' + movie.id + '?source=' + (movie.source || 'local') + '" class="movie-card">' +
                    '<div class="movie-poster">' + poster +
                    '<div class="rating-badge">⭐ ' + movie.rating + '</div></div>' +
                    '<div class="movie-info"><h3 class="movie-title">' + movie.title + '</h3>' +
                    '<p class="movie-year">' + year + '</p></div></a>';
            });
            container.innerHTML = html;
        })
        .catch(function () {
            container.innerHTML = '<p style="text-align:center; color:#9CA3AF;">Error loading movies.</p>';
        });
}


// =================== TOAST NOTIFICATION ===================
function showToast(message) {
    var toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(function () {
        toast.classList.remove('show');
    }, 2500);
}
