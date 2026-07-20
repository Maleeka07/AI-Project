"""Fix remaining 3 movie posters that failed."""
import os
import requests
from models import db

POSTERS_DIR = 'static/images/posters'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Alternative URLs for the 3 failed movies
REMAINING = {
    'Forrest Gump': [
        'https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNjU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
        'https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg',
    ],
    'The Matrix': [
        'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNlYzNjNTc4L10BMl5BanBnXkFtZTgwNTQ4MTcxMTE@._V1_SX300.jpg',
        'https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg',
    ],
    'Spider-Man: No Way Home': [
        'https://m.media-amazon.com/images/M/MV5BZWMyYzFjYTYtNTRjYi00OGExLWE2YzgtOGRmYjFkZmNiMmJiXkEyXkFqcGc@._V1_SX300.jpg',
        'https://upload.wikimedia.org/wikipedia/en/0/00/Spider-Man_No_Way_Home_poster.jpg',
    ],
}

def download_poster(title, urls):
    slug = title.lower().replace(' ', '_').replace(':', '').replace('-', '_').replace("'", '') + '.jpg'
    filepath = os.path.join(POSTERS_DIR, slug)
    
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200 and len(response.content) > 1000:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"  OK: {title} -> {filepath} ({len(response.content)} bytes) from {url[:50]}...")
                return f"images/posters/{slug}"
            else:
                print(f"  SKIP: {title} - Status {response.status_code} from {url[:50]}...")
        except Exception as e:
            print(f"  ERROR: {title} - {e}")
    
    return None

def main():
    print("Fixing remaining 3 posters...")
    for title, urls in REMAINING.items():
        result = download_poster(title, urls)
        if result:
            db.execute_update("UPDATE movies SET poster_path = %s WHERE title = %s", (result, title))
            print(f"  DB updated for {title}")
        else:
            print(f"  FAILED ALL URLS for {title}")

if __name__ == '__main__':
    main()
