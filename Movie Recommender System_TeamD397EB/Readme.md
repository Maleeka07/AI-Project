# AI-Powered Movie Recommendation Engine 🎬

A production-ready, full-stack movie recommendation platform built with Python, Flask, and MySQL. This system provides an intelligent, personalized movie discovery experience by leveraging a custom Machine Learning recommendation engine (TF-IDF & Cosine Similarity) that learns from user behavior, watch history, and preferences.

The application is designed to be highly resilient, seamlessly switching between an **Online Mode** (fetching live data via the TMDB API) and an **Offline Mode** (serving movies and running AI algorithms entirely from a local MySQL database).

![Dashboard Preview](docs/images/dashboard_preview.png)
*(Placeholder: Dashboard Preview Image)*

---

## 🌟 Key Features

* **Hybrid AI Recommendation Engine:** Calculates recommendation scores using a hybrid approach:
  * 40% User Behavior (Watch history, favorites, genre preferences)
  * 30% Content Similarity (TF-IDF matching on overview, keywords, cast, and director)
  * 20% Genre Overlap
  * 10% Global Popularity
* **Explainable AI (XAI):** Tells the user *why* a movie is recommended (e.g., "✓ 92% Match", "✓ Because you watched Inception", "✓ Similar Story").
* **Smart Search:** Includes fuzzy searching, typo tolerance, and autocomplete suggestions.
* **Mood-Based Discovery:** Get instant recommendations based on your current mood (Happy, Sad, Thriller, etc.).
* **Admin Dashboard:** A built-in management interface to add, edit, and organize local movies without writing a single line of code.
* **Resilient Offline Architecture:** A background script pre-downloads posters and stores movie metadata locally, ensuring the platform works flawlessly without an internet connection.

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, Vanilla CSS3 (Glassmorphism, Dark Mode), Vanilla JavaScript
* **Backend:** Python 3.12+, Flask
* **Database:** MySQL
* **Machine Learning / AI:** Scikit-Learn, Pandas, NumPy
* **Utilities:** RapidFuzz (for Typo Correction), Requests

---

## 🚀 Getting Started

Follow these step-by-step instructions to get the project running on your local machine.

### 1. Prerequisites

Make sure you have the following installed on your system:
* **Python (3.8 or higher)**
* **XAMPP** (or any standalone MySQL server)
* **Git** (optional, for cloning)

### 2. Database Setup

1. Open the **XAMPP Control Panel** and start the **MySQL** module.
2. Open your browser and go to `http://localhost/phpmyadmin`.
3. Create a new database or simply go to the **Import** tab.
4. Select the `database.sql` file located in the root directory of this project and click **Import**. This will create all necessary tables (`users`, `movies`, `genres`, etc.) and insert the initial testing data.

### 3. Environment & Dependencies

Open your terminal or command prompt in the project's root directory and run:

```bash
# It is highly recommended to use a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Install all required Python packages
pip install -r requirements.txt
```

### 4. Configuration (Optional)

Open `config.py` in your code editor. By default, it connects to a standard XAMPP local MySQL instance (`root` user with no password). 
If you want to use the **Online Mode**, insert your TMDB API Key:
```python
TMDB_API_KEY = 'your_api_key_here'
```

### 5. Fetching Offline Assets

To ensure you have a complete local catalog (including posters), run the following scripts. This will populate your local `static/images/posters/` folder and generate thousands of test movies:

```bash
# 1. Generate additional movies for testing the AI
python generate_movies.py

# 2. Download posters for offline access
python download_offline_posters.py

# 3. Synchronize database image paths
python fix_paths.py
```

### 6. Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will start running at `http://127.0.0.1:5000`.

---

## 📸 Screenshots

### Homepage & Mood Selector
![Homepage](docs/images/homepage.png)
*(Placeholder: Homepage showing trending movies and mood selectors)*

### Movie Details & Explainable AI
![Movie Details](docs/images/movie_details.png)
*(Placeholder: Movie detail page showing "Recommended Because..." tags)*

### Admin Dashboard
![Admin Dashboard](docs/images/admin_panel.png)
*(Placeholder: Admin panel for managing local movie database)*

---

## 🧠 How the AI Engine Works

The core of the system is the `RecommendationEngine` class located in `ai/recommendation.py`. 
When a user interacts with a movie, their `UserProfile` aggregates their top genres, actors, and directors. The AI Engine then generates a TF-IDF matrix using `scikit-learn` across the entire movie database. 

By calculating the **Cosine Similarity** between movies and combining it with the user's historical behavior score, the system delivers highly accurate, personalized, and explainable recommendations.

---

## 📄 License

This is an open-source project created for educational purposes. Feel free to fork, modify, and build upon it!
