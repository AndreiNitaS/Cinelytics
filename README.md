# Data Warehousing

## Introduction
Welcome to Cinelytics, a modern platform where movie lovers can rate, review, and track the films they watch.

## Business requirements
The platform is designed to track users loved (or hated) movies, also giving them our recommandations based on comumunity ratings.

### Our Business Goals
1. **Evaluate Movie Reception Based on Community Ratings** - Categorize movies as “loved” or “hated” by analyzing community ratings and user reactions, helping users discover high-quality or controversial content.
Bonus category: Bad movies that you want to watch.
2. **Benchmark Movies Against Community Sentiment** - Compare internal user feedback with aggregated external ratings (IMDb, TMDb) to detect overhyped or underrated content.
3. **Provide a Friend Section** - Compare your ratings with your friends to keep the connection alive.

## Reports
Loved vs Hated Movies by Genre
Your Ratings vs Community Average
Friend Score Mismatches(**Warning:** We do not take responsability for the upcoming fights!)


## Dashboards
Real-time list of movies gaining traction in the last 7 days
Visual comparison between the number of movies recommended, how many were actually watched, and how users rated them afterward.
An interactive radar chart showing how each genre performs in terms of positive vs negative user ratings


## KPIs
Friend Disagreement Index
Loved-to-Hated Ratio
Recommendation Acceptance Rate (%)
Rating Drift Over Time



# How to Run the Project

## 1. Prerequisites
Make sure you have:
- **Python 3.10+** installed  
- **PostgreSQL** running locally (or in Docker)  
- A **TMDb API Key** (get one for free at [This API](https://www.themoviedb.org/settings/api))

## 2. Clone or Create Project Folder
If you have the source code, just extract it to a folder:

Inside it, you should see:

Cinelytics/
├── src/
│ ├── extract/
│ ├── transform/
│ ├── data/
│ ├── run_pipeline.py
│ └── interface.py
├── requirements.txt
└── README.md

## 3. Install Dependencies

pip install -r requirements.txt

## 4. Set Up the .env File

In the root Cinelytics folder, create a file named .env:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=cinelytics
DB_USER=postgres
DB_PASSWORD=your_password
TMDB_API_KEY=your_tmdb_key_here


## 5. Prepare the Database

CREATE SCHEMA raw;
CREATE SCHEMA staging;
CREATE SCHEMA trusted;


## 6. Run the Pipeline

python run_pipeline.py


# Data Warehousing Design

## Sources
Cinelytics - Own Platform data.
TMDb (The Movie Database) API
IMDb API (via RapidAPI)
TasteDive API
Open Movie Database (OMDb) API

## Cinelytics source

### TMDb API  (schema: raw)

#### `movieMetadata`
| Column        | Type       | Description                             |
|---------------|------------|-----------------------------------------|
| movieid       | INT        | Unique movie identifier                 |
| title         | VARCHAR    | Movie title                             |
| genre         | VARCHAR    | Primary genre                           |
| releaseyear   | INT        | Year the movie was released             |
| tmdbvotes     | INT        | Number of votes on TMDb                 |
| vote_average  | NUMERIC    | Average TMDb rating (vote_average)      |

### IMDB API (schema: raw)

#### `imdbRatings`
| Column     | Type       | Description                      |
|------------|------------|----------------------------------|
| movieid    | INT        | Foreign key to moviemetadata     |
| imdbrating | NUMERIC    | IMDb average rating              |
| imdbvotes  | INT        | Total votes on IMDb              |



### `coolTable_movie_ratings` (schema: staging)

| Column        | Type         | Description                                             |
|---------------|--------------|---------------------------------------------------------|
| movieid       | INT          | Unique movie ID (from raw.moviemetadata)               |
| title         | VARCHAR      | Movie title                                             |
| genre         | VARCHAR      | Genre                                                   |
| releaseyear   | INT          | Year of release                                         |
| tmdbvotes     | INT          | Number of votes on TMDb                                 |
| avg_rating    | NUMERIC(3,2) | Average rating from internal users                      |
| total_ratings | INT          | Total number of ratings from internal users             |




### `movie_reception` (schema: trusted)

| Column              | Type        | Description                                                              |
|---------------------|-------------|--------------------------------------------------------------------------|
| movieid             | INT         | Unique movie ID (same as in raw.moviemetadata)                           |
| title               | VARCHAR     | Movie title                                                              |
| genre               | VARCHAR     | Movie genre                                                              |
| avg_rating          | NUMERIC(3,2)| Average rating from internal user ratings                                |
| total_ratings       | INT         | Number of ratings from internal users                                    |
| tmdbvotes           | INT         | Number of votes on TMDb                                                  |
| tmdb_avg            | NUMERIC(3,1)| Average rating from TMDb (vote_average from raw.moviemetadata)          |
| category            | VARCHAR     | Classification: Loved / Hated / So bad it's good / Neutral               |




##ETL Pipeline Overview
##Extract:
###Fetch movie data and user ratings from TMDb API and internal CSV sources.

##Transform:
###Aggregate ratings, compute averages, and identify category thresholds.

##Load:
###Populate the staging and trusted schemas for analytical reporting.





