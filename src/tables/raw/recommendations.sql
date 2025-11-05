CREATE TABLE IF NOT EXISTS raw.recommendations (
    userid       INT,
    movieid      INT,
    recommended_ts BIGINT,
    PRIMARY KEY (userid, movieid)
);
