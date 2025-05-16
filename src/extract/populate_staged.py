import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from src.extract.db_config import get_connection

def populate_coolTable_movie_ratings():
    conn = get_connection()
    crs = conn.cursor()

    crs.execute("""
        INSERT INTO staging.coolTable_movie_ratings (
            movieid, title, genre, releaseyear, tmdbvotes, avg_rating, total_ratings
        )
        SELECT
            m.movieid,
            m.title,
            m.genre,
            m.releaseyear,
            m.tmdbvotes,
            ROUND(AVG(r.rating), 2) AS avg_rating,
            COUNT(r.rating) AS total_ratings
        FROM raw.moviemetadata m
        JOIN raw.userratings r ON m.movieid = r.movieid
        GROUP BY m.movieid, m.title, m.genre, m.releaseyear, m.tmdbvotes
        ON CONFLICT (movieid) DO UPDATE
        SET avg_rating = EXCLUDED.avg_rating,
            total_ratings = EXCLUDED.total_ratings;
    """)

    conn.commit()
    crs.close()
    conn.close()
    #print("coolTable_movie_ratings has been populated.") - this is only for testing purposes

if __name__ == "__main__":
    populate_coolTable_movie_ratings()

    
