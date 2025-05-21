import time
import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .db_config import get_connection

def recommend_similar_movies(target_movie_id, user_id, limit=10):
    TMDB_KEY = os.getenv("TMDB_API_KEY")
    if not TMDB_KEY:
        raise RuntimeError("TMDB key missing")

    res = requests.get(
        f"https://api.themoviedb.org/3/movie/{target_movie_id}/similar",
        params={"api_key": TMDB_KEY, "language": "en-US", "page": 1}
    ).json()

    if "results" not in res or not res["results"]:
        return []

    similar = res["results"][:limit]

    conn = get_connection()
    crs = conn.cursor()

    now_ts = int(time.time())
    recommendations = []

    for movie in similar:
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
            INSERT INTO raw.moviemetadata (movieid, title, genre, releaseyear, tmdbvotes, vote_average)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (movieid) DO NOTHING;
        """, (
            tmdb_id,
            title,
            genre,
            release_year,
            movie["vote_count"],
            vote_average
        ))

        crs.execute("""
            INSERT INTO raw.recommendations (userid, movieid, recommended_ts)
            VALUES (%s, %s, %s)
            ON CONFLICT (userid, movieid) DO NOTHING;
        """, (user_id, tmdb_id, now_ts))

        recommendations.append((tmdb_id, title, vote_average))

    conn.commit()
    crs.close()
    conn.close()

    return recommendations
