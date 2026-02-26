# Cinelytics Web Application

A modern web-based movie rating and recommendation system built with Flask.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Virtual environment (recommended)

### Installation

1. **Activate your virtual environment** (if you haven't already):
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up your database configuration**:
   - Make sure your PostgreSQL database is running
   - Update the database configuration in `src/extract/db_config.py` if needed

4. **Initialize the database** (if not done already):
   ```powershell
   cd Cinelytics\src
   python extract/create_tables.py
   python extract/insert_data.py
   ```

### Running the Web Application

1. **Navigate to the src directory**:
   ```powershell
   cd Cinelytics\src
   ```

2. **Run the Flask application**:
   ```powershell
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📱 Features

### User Authentication
- **Sign Up**: Create a new account with username and password
- **Log In**: Secure authentication with bcrypt password hashing
- **Session Management**: Persistent login sessions

### Movie Rating
- **Interactive Rating Slider**: Visual 1-5 star rating system with dynamic canvas animation
- **Movie Search**: Rate any movie from the database
- **TMDb Integration**: View TMDb ratings alongside your ratings

### Recommendations
- **Personalized Suggestions**: Get movie recommendations based on your ratings
- **Similar Movies**: Discover movies similar to ones you've rated

### My Movies
- **View History**: See all movies you've rated
- **Timestamps**: Track when you rated each movie
- **Quick Access**: Easy-to-read list with ratings and dates

## 🎨 Design

The web interface maintains the aesthetic of the original Tkinter application with:
- Clean, modern UI inspired by Apple's design language
- Responsive layout that works on desktop and mobile
- Smooth animations and transitions
- Color scheme: #007aff (accent), #34c759 (success), #ff3b30 (danger)

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: PostgreSQL with psycopg2
- **Authentication**: bcrypt for password hashing
- **Sessions**: Flask session management

## 📁 Project Structure

```
src/
├── app.py                    # Main Flask application
├── templates/                # HTML templates
│   ├── base.html            # Base template with header/footer
│   ├── login.html           # Login and signup page
│   └── main.html            # Main application interface
├── static/                   # Static files
│   ├── css/
│   │   └── style.css        # Application styles
│   └── js/
│       └── app.js           # Client-side JavaScript
└── extract/                  # Database and API modules
    ├── auth.py              # Authentication functions
    ├── rate_movie.py        # Movie rating logic
    ├── recommend_movies.py  # Recommendation engine
    └── my_movies.py         # User movie history
```

## 🔐 Security Notes

- The default `SECRET_KEY` is for development only
- For production, set the `SECRET_KEY` environment variable:
  ```powershell
  $env:SECRET_KEY = "your-secret-key-here"
  ```
- Passwords are hashed using bcrypt
- SQL injection protection via parameterized queries

## 🐛 Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials in `src/extract/db_config.py`
- Ensure database tables are created

### Port Already in Use
- Change the port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### Module Import Errors
- Make sure you're in the correct directory (`Cinelytics\src`)
- Verify all dependencies are installed: `pip install -r requirements.txt`

## 📝 API Endpoints

- `GET /` - Redirect to login or main page
- `GET/POST /login` - User login
- `POST /signup` - Create new account
- `GET /logout` - Logout and clear session
- `GET /main` - Main application page (requires login)
- `POST /api/rate` - Rate a movie and get recommendations (JSON API)
- `GET /api/my-movies` - Get user's rated movies (JSON API)

## 🔄 Migrating from Desktop App

The web application provides the same functionality as the Tkinter desktop version:
- All database functions remain unchanged
- User authentication works identically
- Movie rating and recommendation logic is preserved
- The interface is now accessible from any web browser

## 📄 License

My Little License (as noted in the original application)

---

**Happy rating! 🎬⭐**
