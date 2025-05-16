CREATE TABLE IF NOT EXISTS trusted.movie_reception (
    movieid               INT PRIMARY KEY,
    title                 VARCHAR,
    genre                 VARCHAR,
    avg_rating            NUMERIC(3, 2),
    total_ratings         INT,
    tmdbvotes             INT,
    tmdb_avg              NUMERIC(3, 1),  
    category              VARCHAR
);