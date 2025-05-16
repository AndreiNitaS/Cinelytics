import os
import requests
import random
import argparse
from faker import Faker
from db_config import get_connection
from dotenv import load_dotenv

# This script allows a user to rate a movie and stores the rating in a PostgreSQL database.
# It uses the TMDb API to search for the movie and fetch its metadata.

genre_map = {
    28: "Action", 12: "Adventure", 16: "Animation",
    35: "Comedy", 80: "Crime", 99: "Documentary",
    18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
    27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller",
    10752: "War", 37: "Western"
}

load_dotenv()
fake = Faker()

def rate_movie(movie_title, your_rating):
    user_name = fake.user_name()
    user_id = random.randint(1_000, 9_999)

    print(f"👤 Your random user is: {user_name} (id={user_id})")

    TMDB_KEY = os.getenv("TMDB_API_KEY")
    if not TMDB_KEY:
        raise RuntimeError("You need to put the correct TMDB key in the .env file")

    search = requests.get(
        "https://api.themoviedb.org/3/search/movie",
        params={"api_key": TMDB_KEY, "query": movie_title}
    ).json()

    if not search.get("results"):
        print("Movie is not found on TMDb.")
        exit(1)

    film = search["results"][0]
    tmdb_id = film["id"]
    community_rating = film["vote_average"]
    print(f"🎥 Found on TMDb: {film['title']} ({film['release_date'][:4]}), community rating: {community_rating}")

    conn = get_connection()
    crs = conn.cursor()

    crs.execute(
        "INSERT INTO raw.moviemetadata(movieid, title, genre, releaseyear, tmdbvotes, vote_average) "
        "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (movieid) DO NOTHING",
        (
            tmdb_id,
            film["title"],
            genre_map.get(film["genre_ids"][0], "Unknown") if film.get("genre_ids") else "Unknown",
            int(film["release_date"][:4]) if film.get("release_date") else None,
            film["vote_count"],
            film["vote_average"]

        )
    )

    crs.execute(
        "INSERT INTO raw.userratings(userid, movieid, rating, rating_ts) "
        "VALUES (%s,%s,%s,extract(epoch from now())::bigint) "
        "ON CONFLICT (userid,movieid) DO UPDATE SET rating = EXCLUDED.rating",
        (
            user_id,
            tmdb_id,
            int(your_rating)
        )
    )

    conn.commit()
    crs.close()
    conn.close()

    print("Your rating has been saved!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--movie", type=str, help="Movie title")
    parser.add_argument("--rating", type=int, help="Your rating (1–5)")
    args = parser.parse_args()

    if args.movie is not None and args.rating is not None:
        rate_movie(args.movie, args.rating)
    else:
        movie_title = input("🎬 Enter movie title: ").strip()
        your_rating = input("⭐ Your rating (1–5): ").strip()
        rate_movie(movie_title, your_rating)
