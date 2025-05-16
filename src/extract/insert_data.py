
import csv
from src.extract.db_config import get_connection

def insert_movie_metadata(path="data/movie_metadata.csv"):
    conn = get_connection()
    crs  = conn.cursor()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            crs.execute(
                """
                INSERT INTO raw.moviemetadata
                  (movieid, title, genre, releaseyear, tmdbvotes)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (movieid) DO NOTHING
                """,
                (
                    int(row["movieId"]),
                    row["title"],
                    row["genre"],
                    int(row["releaseYear"]),
                    int(row["tmdbVotes"])
                )
            )
    conn.commit()
    crs.close()
    conn.close()

def insert_user_ratings(path="data/user_ratings.csv"):
    conn = get_connection()
    crs  = conn.cursor()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            crs.execute(
                """
                INSERT INTO raw.userratings
                  (userid, movieid, rating, timestamp)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (userid, movieid) DO NOTHING
                """,
                (
                    int(row["userId"]),
                    int(row["movieId"]),
                    int(row["rating"]),
                    int(row["timestamp"])
                )
            )
    conn.commit()
    crs.close()
    conn.close()


def main():
    insert_movie_metadata()
    insert_user_ratings()
    print("Test data inserted.")

if __name__ == "__main__":
    main()
