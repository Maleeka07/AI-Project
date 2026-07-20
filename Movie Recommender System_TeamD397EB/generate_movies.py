import random
import requests
from models import db, movie_model

# 1. Real TMDB Poster URLs for existing 15 sample movies
EXISTING_POSTERS = {
    'The Dark Knight': 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
    'Inception': 'https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg',
    'Avengers: Endgame': 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg',
    'Interstellar': 'https://image.tmdb.org/t/p/w500/gEU2QlsUUHXjNpeMacBj122Q9nj.jpg',
    'The Godfather': 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg',
    'Pulp Fiction': 'https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPbOYKQru12.jpg',
    'Forrest Gump': 'https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg',
    'The Matrix': 'https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
    'Titanic': 'https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg',
    'Jurassic Park': 'https://image.tmdb.org/t/p/w500/oU7Oq2kFAAlGqbU4VoJlPzQ6Z6c.jpg',
    'Iron Man': 'https://image.tmdb.org/t/p/w500/78lPtwv72eTNqFW9O53WEJMUGPN.jpg',
    'Spider-Man: No Way Home': 'https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1ZrsNbjKntF05Q.jpg',
    'The Shawshank Redemption': 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg',
    'Frozen': 'https://image.tmdb.org/t/p/w500/kGVn6u0R0Oq9yDqY1u64t7XG7K6.jpg',
    'The Conjuring': 'https://image.tmdb.org/t/p/w500/b0zQk8zGq3zF5Dk4m0rA5r4y8c9.jpg'
}

# 2. Movie Generation Data
PREFIXES = ["The", "A", "Return of the", "Rise of the", "Fall of", "Beyond the", "Secrets of", "Legend of", "Last", "First", "Dark", "Lost", "Hidden", "Silent"]
NOUNS = ["Warrior", "King", "Queen", "Knight", "Ghost", "Alien", "Monster", "City", "World", "Star", "Planet", "Sword", "Shadow", "Dream", "Time", "Blood", "Heart", "Soul", "Journey"]
SUFFIXES = ["Part I", "Part II", "The Beginning", "Endgame", "Reborn", "Unleashed", "Origins", "Awakening", "Legacy", "Forever"]

GENRES_LIST = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Family', 'Fantasy', 'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Documentary']

def generate_title(genre):
    p = random.choice(PREFIXES)
    n = random.choice(NOUNS)
    
    if random.random() > 0.7:
        s = random.choice(SUFFIXES)
        return f"{p} {n}: {s}"
    else:
        return f"{p} {n}"

def update_existing_posters():
    """Update existing movies with real posters."""
    print("Updating existing 15 movies with real posters...")
    movies = movie_model.get_all_movies()
    for m in movies:
        if m['title'] in EXISTING_POSTERS:
            poster = EXISTING_POSTERS[m['title']]
            db.execute_update("UPDATE movies SET poster_path = %s WHERE id = %s", (poster, m['id']))
    print("Existing posters updated!")

def generate_1500_movies():
    """Generate 100+ movies per genre."""
    print("Generating 1500+ movies (this will take a few seconds)...")
    
    # We will generate 105 movies for each of the 15 genres = 1575 movies
    for genre in GENRES_LIST:
        print(f"Generating 105 movies for {genre}...")
        for i in range(105):
            title = generate_title(genre)
            # Add a random unique identifier so titles don't completely overlap
            title = f"{title} ({random.randint(1000, 9999)})"
            
            year = random.randint(1990, 2024)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            release_date = f"{year}-{month:02d}-{day:02d}"
            
            runtime = random.randint(85, 180)
            rating = round(random.uniform(4.0, 9.5), 1)
            popularity = round(random.uniform(10.0, 100.0), 1)
            
            # Using Placehold.co for poster images so it loads without error
            # Format: https://placehold.co/300x450/222222/FFF?text=Movie+Title
            safe_title = title.replace(' ', '+').replace(':', '')
            poster_path = f"https://placehold.co/300x450/333333/FFFFFF?text={safe_title}"
            
            # Insert movie directly
            movie_id = db.execute_update("""
                INSERT INTO movies (title, overview, release_date, runtime, rating, language,
                    poster_path, popularity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                title, 
                f"An amazing {genre.lower()} movie about a {random.choice(NOUNS).lower()}.", 
                release_date, runtime, rating, 'en', poster_path, popularity
            ))
            
            # Get genre id
            g_rows = db.execute_query("SELECT id FROM genres WHERE name = %s", (genre,))
            if g_rows:
                g_id = g_rows[0]['id']
                db.execute_update("INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, g_id))
                
                # Assign 1 or 2 extra random genres occasionally
                if random.random() > 0.5:
                    extra = random.choice(GENRES_LIST)
                    if extra != genre:
                        e_rows = db.execute_query("SELECT id FROM genres WHERE name = %s", (extra,))
                        if e_rows:
                            db.execute_update("INSERT IGNORE INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, e_rows[0]['id']))

    print("Generation complete! Total movies added: 1575.")

if __name__ == '__main__':
    update_existing_posters()
    generate_1500_movies()
