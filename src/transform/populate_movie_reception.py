import os
import sys
import psycopg2

# Adaugă calea pentru importul conexiunii DB
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "extract")))
from db_config import get_connection

def read_sql(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def execute_query(sql):
    conn = get_connection()
    crs = conn.cursor()
    crs.execute(sql)
    conn.commit()
    crs.close()
    conn.close()

# INSERT final fără alte dependențe
SQL_INSERT = """
INSERT INTO trusted.movie_reception (
    movieid, title, genre, avg_rating, total_ratings, tmdbvotes, tmdb_avg, category
)
SELECT
    m.movieid,
    m.title,
    m.genre,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.rating) AS total_ratings,
    m.tmdbvotes,
    m.vote_average,
    CASE
        WHEN ROUND(AVG(r.rating), 2) >= 4.5 THEN 'Loved'
        WHEN ROUND(AVG(r.rating), 2) <= 2.0 THEN 'Hated'
        WHEN ROUND(AVG(r.rating), 2) <= 3.0 AND m.vote_average >= 6.5 THEN 'So bad it’s good'
        ELSE 'Neutral'
    END AS category
FROM raw.moviemetadata m
JOIN raw.userratings r ON m.movieid = r.movieid
WHERE m.vote_average IS NOT NULL
GROUP BY m.movieid, m.title, m.genre, m.tmdbvotes, m.vote_average
ON CONFLICT (movieid) DO UPDATE
SET
    avg_rating = EXCLUDED.avg_rating,
    total_ratings = EXCLUDED.total_ratings,
    category = EXCLUDED.category;
"""

if __name__ == "__main__":
    create_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "tables", "trusted", "movie_reception.sql"
))

    execute_query(read_sql(create_path))
    execute_query(SQL_INSERT)
    print("trusted.movie_reception populated.")
