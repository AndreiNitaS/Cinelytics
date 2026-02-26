from db_config import get_connection

#This script creates the raw tables in the SQLite database.

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS moviemetadata (
            movieid      INTEGER PRIMARY KEY,
            title        TEXT,
            genre        TEXT,
            releaseyear  INTEGER,
            tmdbvotes    INTEGER,
            vote_average REAL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS userratings (
            userid       INTEGER,
            movieid      INTEGER,
            rating       INTEGER,
            rating_ts    INTEGER,
            PRIMARY KEY (userid, movieid)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS users (
            userid        INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS recommendations (
            userid        INTEGER,
            movieid       INTEGER,
            recommended_ts INTEGER,
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
