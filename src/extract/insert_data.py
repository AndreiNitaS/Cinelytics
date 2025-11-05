
import csv

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db_config import get_connection

# This script inserts test data into the PostgreSQL database.
# It reads data from CSV files and inserts it into the raw tables.
# The CSV files are expected to be in the data directory relative to this script's location.

def insert_movie_metadata(path=None):
    if path is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "movie_metadata.csv"))

    conn = get_connection()
    crs = conn.cursor()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vote_avg = float(row["vote_average"]) if "vote_average" in row and row["vote_average"] else None
            crs.execute(
                """
                INSERT INTO raw.moviemetadata
                  (movieid, title, genre, releaseyear, tmdbvotes, vote_average)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (movieid) DO NOTHING
                """,
                (
                    int(row["movieId"]),
                    row["title"],
                    row["genre"],
                    int(row["releaseYear"]),
                    int(row["tmdbVotes"]),
                    vote_avg
                )
            )
    conn.commit()
    crs.close()
    conn.close()

def insert_user_ratings(path=None):
    if path is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "user_ratings.csv"))

    conn = get_connection()
    crs = conn.cursor()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            crs.execute(
                """
                INSERT INTO raw.userratings
                  (userid, movieid, rating, rating_ts)
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