CREATE TABLE IF NOT EXISTS staging.coolTable_movie_ratings (
    movieid         INT PRIMARY KEY,
    title           VARCHAR,
    genre           VARCHAR,
    releaseyear     INT,
    tmdbvotes       INT,
    avg_rating      DECIMAL,
    total_ratings   INT
);
