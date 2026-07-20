-- AI-Powered Movie Recommendation Feed Database
-- Import this file in phpMyAdmin

CREATE DATABASE IF NOT EXISTS movie_recommendation_db;
USE movie_recommendation_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Movies table
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    overview TEXT,
    release_date VARCHAR(20),
    runtime INT DEFAULT 0,
    rating FLOAT DEFAULT 0,
    language VARCHAR(50) DEFAULT 'en',
    poster_path VARCHAR(500),
    trailer_link VARCHAR(500),
    trailer_file VARCHAR(500),
    keywords TEXT,
    popularity FLOAT DEFAULT 0,
    director VARCHAR(200),
    production_company VARCHAR(200),
    tmdb_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Genres table
CREATE TABLE IF NOT EXISTS genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Actors table
CREATE TABLE IF NOT EXISTS actors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);

-- Directors table
CREATE TABLE IF NOT EXISTS directors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);

-- Movie-Genre link
CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id INT,
    genre_id INT,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);

-- Movie-Actor link
CREATE TABLE IF NOT EXISTS movie_actors (
    movie_id INT,
    actor_id INT,
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE CASCADE
);

-- Search History
CREATE TABLE IF NOT EXISTS search_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    query VARCHAR(255),
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Watch History
CREATE TABLE IF NOT EXISTS watch_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

-- Favorites
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

-- Ratings
CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    movie_id INT,
    rating FLOAT,
    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
);

-- User Preferences (AI Profile)
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INT PRIMARY KEY,
    preferred_genres TEXT,
    preferred_actors TEXT,
    preferred_directors TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- SAMPLE DATA
-- ============================================

-- Default user
INSERT INTO users (username) VALUES ('default_user');

-- Genres
INSERT INTO genres (name) VALUES
('Action'), ('Adventure'), ('Animation'), ('Comedy'), ('Crime'),
('Drama'), ('Family'), ('Fantasy'), ('Horror'), ('Mystery'),
('Romance'), ('Sci-Fi'), ('Thriller'), ('War'), ('Documentary');

-- Sample Movies
INSERT INTO movies (title, overview, release_date, runtime, rating, language, poster_path, trailer_link, keywords, popularity, director, production_company) VALUES
('The Dark Knight', 'When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest tests to fight injustice.', '2008-07-18', 152, 9.0, 'en', '', 'https://www.youtube.com/watch?v=EXeTwQWrcwY', 'batman,joker,gotham,superhero,crime', 95.5, 'Christopher Nolan', 'Warner Bros'),
('Inception', 'A thief who steals corporate secrets through dream-sharing technology is given the task of planting an idea into the mind of a C.E.O.', '2010-07-16', 148, 8.8, 'en', '', 'https://www.youtube.com/watch?v=YoHD9XEInc0', 'dream,heist,subconscious,mind,thriller', 90.2, 'Christopher Nolan', 'Warner Bros'),
('Avengers: Endgame', 'After the devastating events of Infinity War, the Avengers assemble once more to reverse Thanos actions and restore balance.', '2019-04-26', 181, 8.4, 'en', '', 'https://www.youtube.com/watch?v=TcMBFSGVi1c', 'avengers,thanos,marvel,superhero,time travel', 98.0, 'Anthony Russo', 'Marvel Studios'),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanitys survival.', '2014-11-07', 169, 8.6, 'en', '', 'https://www.youtube.com/watch?v=zSWdZVtXT7E', 'space,wormhole,time,survival,nasa', 88.5, 'Christopher Nolan', 'Paramount'),
('The Godfather', 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.', '1972-03-24', 175, 9.2, 'en', '', 'https://www.youtube.com/watch?v=sY1S34973zA', 'mafia,family,crime,power,godfather', 85.0, 'Francis Ford Coppola', 'Paramount'),
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.', '1994-10-14', 154, 8.9, 'en', '', 'https://www.youtube.com/watch?v=s7EdQ4FqbhY', 'crime,hitman,gangster,nonlinear,violence', 82.3, 'Quentin Tarantino', 'Miramax'),
('Forrest Gump', 'The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man.', '1994-07-06', 142, 8.8, 'en', '', 'https://www.youtube.com/watch?v=bLvqoHBptjg', 'life,vietnam,running,love,history', 80.1, 'Robert Zemeckis', 'Paramount'),
('The Matrix', 'A computer hacker learns about the true nature of his reality and his role in the war against its controllers.', '1999-03-31', 136, 8.7, 'en', '', 'https://www.youtube.com/watch?v=vKQi3bBA1y8', 'matrix,simulation,hacker,ai,martial arts', 87.9, 'Lana Wachowski', 'Warner Bros'),
('Titanic', 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious Titanic.', '1997-12-19', 194, 7.9, 'en', '', 'https://www.youtube.com/watch?v=2e-eXJ6HgkQ', 'ship,love,disaster,ocean,romance', 78.5, 'James Cameron', '20th Century Fox'),
('Jurassic Park', 'A pragmatic paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after the parks genetically engineered dinosaurs break free.', '1993-06-11', 127, 8.1, 'en', '', 'https://www.youtube.com/watch?v=lc0UehYemQA', 'dinosaur,theme park,genetic,adventure,island', 76.8, 'Steven Spielberg', 'Universal'),
('Iron Man', 'After being held captive in an Afghan cave, billionaire engineer Tony Stark creates a unique weaponized suit of armor to fight evil.', '2008-05-02', 126, 7.9, 'en', '', 'https://www.youtube.com/watch?v=8ugaeA-nMTc', 'iron man,tony stark,marvel,superhero,armor', 83.2, 'Jon Favreau', 'Marvel Studios'),
('Spider-Man: No Way Home', 'With Spider-Mans identity now revealed, Peter asks Doctor Strange for help. When a spell goes wrong, dangerous foes from other worlds appear.', '2021-12-17', 148, 8.3, 'en', '', 'https://www.youtube.com/watch?v=JfVOs4VSpmA', 'spider-man,multiverse,marvel,superhero,magic', 91.0, 'Jon Watts', 'Marvel Studios'),
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', '1994-09-23', 142, 9.3, 'en', '', 'https://www.youtube.com/watch?v=6hB3S9d6mZ0', 'prison,hope,friendship,redemption,escape', 84.0, 'Frank Darabont', 'Castle Rock'),
('Frozen', 'When the newly crowned Queen Elsa accidentally uses her power to turn things into ice, her sister Anna teams up with a mountain man to change the weather.', '2013-11-27', 102, 7.4, 'en', '', 'https://www.youtube.com/watch?v=TbQm5doF_Uc', 'frozen,ice,princess,sister,magic,animation', 75.3, 'Chris Buck', 'Walt Disney'),
('The Conjuring', 'Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.', '2013-07-19', 112, 7.5, 'en', '', 'https://www.youtube.com/watch?v=k10ETZ41q5o', 'horror,ghost,haunted,paranormal,demon', 72.1, 'James Wan', 'New Line Cinema');

-- Actors
INSERT INTO actors (name) VALUES
('Christian Bale'), ('Heath Ledger'), ('Leonardo DiCaprio'), ('Joseph Gordon-Levitt'),
('Robert Downey Jr.'), ('Chris Evans'), ('Scarlett Johansson'),
('Matthew McConaughey'), ('Anne Hathaway'), ('Marlon Brando'),
('Al Pacino'), ('John Travolta'), ('Samuel L. Jackson'),
('Tom Hanks'), ('Keanu Reeves'), ('Kate Winslet'),
('Sam Neill'), ('Tom Holland'), ('Zendaya'),
('Tim Robbins'), ('Morgan Freeman'), ('Kristen Bell'), ('Vera Farmiga');

-- Directors
INSERT INTO directors (name) VALUES
('Christopher Nolan'), ('Anthony Russo'), ('Francis Ford Coppola'),
('Quentin Tarantino'), ('Robert Zemeckis'), ('Lana Wachowski'),
('James Cameron'), ('Steven Spielberg'), ('Jon Favreau'),
('Jon Watts'), ('Frank Darabont'), ('Chris Buck'), ('James Wan');

-- Movie-Genre links
INSERT INTO movie_genres (movie_id, genre_id) VALUES
(1, 1), (1, 5), (1, 13),
(2, 1), (2, 12), (2, 13),
(3, 1), (3, 2), (3, 12),
(4, 2), (4, 6), (4, 12),
(5, 5), (5, 6),
(6, 5), (6, 13),
(7, 4), (7, 6), (7, 11),
(8, 1), (8, 12),
(9, 6), (9, 11),
(10, 1), (10, 2), (10, 12),
(11, 1), (11, 2), (11, 12),
(12, 1), (12, 2), (12, 12),
(13, 5), (13, 6),
(14, 3), (14, 4), (14, 7),
(15, 9), (15, 13), (15, 10);

-- Movie-Actor links
INSERT INTO movie_actors (movie_id, actor_id) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4),
(3, 5), (3, 6), (3, 7),
(4, 8), (4, 9),
(5, 10), (5, 11),
(6, 12), (6, 13),
(7, 14),
(8, 15),
(9, 3), (9, 16),
(10, 17),
(11, 5),
(12, 18), (12, 19),
(13, 20), (13, 21),
(14, 22),
(15, 23);

-- Default user preferences
INSERT INTO user_preferences (user_id, preferred_genres, preferred_actors, preferred_directors)
VALUES (1, '', '', '');
