# Data Warehousing

## Scenario
You are a Data Engineer at Cinelytics, a startup platform that allows users to rate, review and track the movies they watch.

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


# Data Warehousing Design

## Sources
Cinelytics - Own Platform data.
TMDb (The Movie Database) API
IMDb API (via RapidAPI)
TasteDive API
Open Movie Database (OMDb) API

## Cinelytics source

### TMDb API 

#### `movieMetadata`
| Column       | Type     | Description                    |
|--------------|----------|--------------------------------|
| movieId     | INT      | Movie ID                       |
| title        | VARCHAR  | Movie title                    |
| genre        | VARCHAR  | Primary genre                  |
| releaseYear | INT       | Year the movie was released    |
| tmdbVotes   | INT       | Number of votes on TMDb        |

### IMDB API

#### `imdbRatings`
| Column       | Type     | Description             |
|--------------|----------|-------------------------|
| movieId     | INT      | Movie ID                |
| imdbRating  | DECIMAL  | Avg. IMDb rating        |
| imdbVotes   | INT      | Vote count on IMDb      |


### TasteDive API

#### `similarMovies`
| Column           | Type     | Description                        |
|------------------|----------|------------------------------------|
| movieId         | INT      | Movie ID                |
| similarId       | INT      | Similar movie ID                   |
| similarityScore | DECIMAL  | Relevance/similarity score         |



###  OMDb API

#### `omdbData`
| Column     | Type     | Description               |
|------------|----------|---------------------------|
| movieId   | INT      | Movie ID                  |
| plot       | TEXT     | Movie description         |
| director   | VARCHAR  | Director                  |

