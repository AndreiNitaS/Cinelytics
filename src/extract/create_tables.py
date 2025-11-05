from db_config import get_connection

#This script creates the raw tables in the PostgreSQL database.

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS raw.moviemetadata (
            movieid      INT PRIMARY KEY,
            title        VARCHAR,
            genre        VARCHAR,
            releaseyear  INT,
            tmdbvotes    INT,
            vote_average   NUMERIC(3, 1)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS raw.userratings (
            userid       INT,
            movieid      INT,
            rating       INT,
            rating_ts    BIGINT,
            PRIMARY KEY (userid, movieid)
        );
        """
    ]

    conn = get_connection()
    crs  = conn.cursor()
    for cmd in commands:
        crs.execute(cmd)
    conn.commit()
    crs.close()
    conn.close()
    print("All raw tables created successfully.")

if __name__ == "__main__":
    create_tables()
