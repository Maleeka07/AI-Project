"""Fix all movie posters - download real posters for all 15 original movies."""
import os
import requests
from models import db

POSTERS_DIR = 'static/images/posters'
os.makedirs(POSTERS_DIR, exist_ok=True)

# Updated working TMDB poster URLs (July 2026)
POSTER_URLS = {
    'The Dark Knight': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg',
    'Inception': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg',
    'Avengers: Endgame': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg',
    'Interstellar': 'https://m.media-amazon.com/images/M/MV5BYzdjMDAxZGItMjI2My00ODA1LTlkNzItOWFjMDU5ZDJlYWY3XkEyXkFqcGc@._V1_SX300.jpg',
    'The Godfather': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
    'Pulp Fiction': 'https://m.media-amazon.com/images/M/MV5BYTViYTE3ZGQtNDBlMC00ZTAyLTkyODMtZGRiZDg0MjA2YThkXkEyXkFqcGc@._V1_SX300.jpg',
    'Forrest Gump': 'https://m.media-amazon.com/images/M/MV5BNDYwNzVjMTYtZmU5YS00YjQ5LTljYjgtMjY2NDVhYWU5NjRiXkEyXkFqcGc@._V1_SX300.jpg',
    'The Matrix': 'https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZDYxZjlhZjhkXkEyXkFqcGc@._V1_SX300.jpg',
    'Titanic': 'https://m.media-amazon.com/images/M/MV5BYzYyN2FiZmUtYWYzMy00MzViLWJkZTMtOGY1ZjgzNWMwN2YxXkEyXkFqcGc@._V1_SX300.jpg',
    'Jurassic Park': 'https://m.media-amazon.com/images/M/MV5BMjM2MDgxMDg0Nl5BMl5BanBnXkFtZTgwNTM2OTM5NDE@._V1_SX300.jpg',
    'Iron Man': 'https://m.media-amazon.com/images/M/MV5BMTczNTI2ODUwOF5BMl5BanBnXkFtZTcwMTU0NTIzMw@@._V1_SX300.jpg',
    'Spider-Man: No Way Home': 'https://m.media-amazon.com/images/M/MV5BZWMyYzFjYTYtNTRjYi00OGExLWE2YzgtOGRmYjFkZmNiMmJiXkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_SX300.jpg',
    'The Shawshank Redemption': 'https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_SX300.jpg',
    'Frozen': 'https://m.media-amazon.com/images/M/MV5BMTQ1MjQwMTE5OF5BMl5BanBnXkFtZTgwNjk3MTcyMDE@._V1_SX300.jpg',
    'The Conjuring': 'https://m.media-amazon.com/images/M/MV5BMTM3NjA1NDMyMV5BMl5BanBnXkFtZTcwMDQzNDMzOQ@@._V1_SX300.jpg',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def download_poster(title, url):
    slug = title.lower().replace(' ', '_').replace(':', '').replace('-', '_').replace("'", '') + '.jpg'
    filepath = os.path.join(POSTERS_DIR, slug)
    
    # Always re-download (overwrite small placeholders)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200 and len(response.content) > 1000:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  OK: {title} -> {filepath} ({len(response.content)} bytes)")
            return f"images/posters/{slug}"
        else:
            print(f"  FAIL: {title} - Status {response.status_code}, Size {len(response.content)}")
    except Exception as e:
        print(f"  ERROR: {title} - {e}")
    
    return None

def main():
    print("=" * 60)
    print("  Downloading Real Movie Posters")
    print("=" * 60)
    
    success = 0
    fail = 0
    
    for title, url in POSTER_URLS.items():
        result = download_poster(title, url)
        if result:
            # Update database with correct local path
            db.execute_update(
                "UPDATE movies SET poster_path = %s WHERE title = %s",
                (result, title)
            )
            success += 1
        else:
            fail += 1
    
    print(f"\nDone! Success: {success}, Failed: {fail}")
    print("Database paths updated.")

if __name__ == '__main__':
    main()
