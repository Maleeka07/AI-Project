import os
import requests
from models import db, movie_model

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

POSTERS_DIR = 'static/images/posters'
DEFAULT_POSTER = '/static/images/posters/default_poster.jpg'

def download_image(url, filename, title=""):
    filepath = os.path.join(POSTERS_DIR, filename)
    if os.path.exists(filepath):
        return f"/{filepath}".replace('\\', '/')
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return f"/{filepath}".replace('\\', '/')
    except Exception as e:
        print(f"Failed to download from TMDB {url}: {e}")
        
    # Fallback to Placehold.co
    safe_title = title.replace(' ', '+').replace(':', '')
    fallback_url = f"https://placehold.co/300x450/333333/FFFFFF.jpg?text={safe_title}"
    try:
        response = requests.get(fallback_url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return f"/{filepath}".replace('\\', '/')
    except Exception as e:
        print(f"Failed to download from Placehold {fallback_url}: {e}")
        
    return DEFAULT_POSTER

def update_all_posters():
    print("Starting offline poster update...")
    movies = db.execute_query("SELECT id, title FROM movies")
    print(f"Found {len(movies)} movies.")
    
    for m in movies:
        title = m['title']
        movie_id = m['id']
        
        # Determine poster path
        if title in EXISTING_POSTERS:
            slug = title.lower().replace(' ', '_').replace(':', '').replace('-', '_') + '.jpg'
            local_path = download_image(EXISTING_POSTERS[title], slug, title)
            print(f"Downloaded {title} -> {local_path}")
        else:
            local_path = DEFAULT_POSTER
            
        # Update DB
        db.execute_update("UPDATE movies SET poster_path = %s WHERE id = %s", (local_path, movie_id))
        
    print("All movies updated to use offline posters!")

if __name__ == '__main__':
    update_all_posters()
