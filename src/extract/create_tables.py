from db_config import get_connection

def create_tables():
    commands = [
        "CREATE SCHEMA IF NOT EXISTS raw;",
        """
        CREATE TABLE IF NOT EXISTS raw.moviemetadata (
            movieid      INT PRIMARY KEY,
            title        VARCHAR,
            genre        VARCHAR,
            releaseyear  INT,
            tmdbvotes    INT
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
        """,
        """
        CREATE TABLE IF NOT EXISTS raw.similarmovies (
            movieid         INT,
            similarid       INT,
            similarityscore DECIMAL,
            PRIMARY KEY (movieid, similarid)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS raw.omdbdata (
            movieid INT PRIMARY KEY,
            plot    TEXT,
            director VARCHAR
        );
        """
    ]

    conn = get_connection()
    cur  = conn.cursor()
    for cmd in commands:
        cur.execute(cmd)
    conn.commit()
    cur.close()
    conn.close()
    print("All raw tables created successfully.")

if __name__ == "__main__":
    create_tables()
