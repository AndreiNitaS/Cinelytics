from src.schemas.db_config import get_connection

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS raw.movieMetadata (
            movieId INT PRIMARY KEY,
            title VARCHAR,
            genre VARCHAR,
            releaseYear INT,
            tmdbVotes INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS raw.imdbRatings (
            movieId INT PRIMARY KEY,
            imdbRating DECIMAL,
            imdbVotes INT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS raw.similarMovies (
            movieId INT,
            similarId INT,
            similarityScore DECIMAL,
            PRIMARY KEY (movieId, similarId)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS raw.omdbData (
            movieId INT PRIMARY KEY,
            plot TEXT,
            director VARCHAR
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS raw.userRatings (
            userId INT,
            movieId INT,
            rating DECIMAL,
            PRIMARY KEY (userId, movieId)
        );
        """
    ]

    conn = get_connection()
    cursor = conn.cursor()
    for command in commands:
        cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
