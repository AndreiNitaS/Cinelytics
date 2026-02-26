import time
import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extract.db_config import get_connection


def recommend_similar_movies(target_movie_id, user_id, limit=10):
    TMDB_KEY = os.getenv("TMDB_API_KEY")
    if not TMDB_KEY:
        raise RuntimeError("TMDB key missing")

    # Get both similar AND recommended movies for better variety
    similar_res = requests.get(
        f"https://api.themoviedb.org/3/movie/{target_movie_id}/similar",
        params={"api_key": TMDB_KEY, "language": "en-US", "page": 1}
    ).json()

    recommend_res = requests.get(
        f"https://api.themoviedb.org/3/movie/{target_movie_id}/recommendations",
        params={"api_key": TMDB_KEY, "language": "en-US", "page": 1}
    ).json()

    # Combine and deduplicate movies
    all_movies = {}
    for movie in similar_res.get("results", []):
        all_movies[movie["id"]] = movie
    for movie in recommend_res.get("results", []):
        all_movies[movie["id"]] = movie

    if not all_movies:
        return []

    # Sort by vote_average (rating) and popularity, then take top results
    sorted_movies = sorted(
        all_movies.values(),
        key=lambda m: (m.get("vote_average", 0), m.get("popularity", 0)),
        reverse=True
    )[:limit]

    conn = get_connection()
    crs = conn.cursor()

    now_ts = int(time.time())
    recommendations = []

    for movie in sorted_movies:
        tmdb_id = movie["id"]
        title = movie["title"]
        vote_average = movie["vote_average"]
        release_date = movie.get("release_date")
        release_year = int(release_date[:4]) if release_date else None
        genre = "Unknown"
        if movie.get("genre_ids"):
            genre_map = {
                28: "Action", 12: "Adventure", 16: "Animation",
                35: "Comedy", 80: "Crime", 99: "Documentary",
                18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
                27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance",
                878: "Science Fiction", 10770: "TV Movie", 53: "Thriller",
                10752: "War", 37: "Western"
            }
            genre = genre_map.get(movie["genre_ids"][0], "Unknown")

        crs.execute("""
            INSERT OR IGNORE INTO moviemetadata (movieid, title, genre, releaseyear, tmdbvotes, vote_average)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (
            tmdb_id,
            title,
            genre,
            release_year,
            movie["vote_count"],
            vote_average
        ))

        crs.execute("""
            INSERT OR IGNORE INTO recommendations (userid, movieid, recommended_ts)
            VALUES (?, ?, ?);
        """, (user_id, tmdb_id, now_ts))

        recommendations.append((tmdb_id, title, vote_average))

    conn.commit()
    crs.close()
    conn.close()

    return recommendations
