"""
Cinelytics Web Application
A Flask-based web interface for rating movies and getting recommendations
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
import os
import sys
import datetime as _dt

# Add path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "Cinelytics", "src"))

from extract.rate_movie import rate_movie
from extract.recommend_movies import recommend_similar_movies
from extract.auth import create_users_table, create_user, authenticate
from extract.my_movies import get_my_movies
from extract.friends import get_friends, add_friend

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize database
try:
    create_users_table()
except Exception as e:
    print(f"Warning: Could not initialize users table: {e}")


def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Redirect to login or main app based on session"""
    if 'user_id' in session:
        return redirect(url_for('main'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        try:
            user_id = authenticate(username, password)
            if user_id:
                session['user_id'] = user_id
                session['username'] = username
                flash(f'Welcome back, {username}!', 'success')
                return redirect(url_for('main'))
            else:
                flash('Invalid username or password', 'error')
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
    
    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    """Create new user account"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if not username or not password:
        flash('Please enter both username and password', 'error')
        return redirect(url_for('login'))
    
    try:
        create_user(username, password)
        flash('Account created successfully! Please log in.', 'success')
    except Exception as e:
        flash(f'Sign up failed: {str(e)}', 'error')
    
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/main')
@login_required
def main():
    """Main application page"""
    return render_template('main.html', username=session.get('username'))


@app.route('/api/rate', methods=['POST'])
@login_required
def rate():
    """API endpoint to rate a movie and get recommendations"""
    data = request.get_json()
    title = data.get('title', '').strip()
    rating = data.get('rating')
    
    if not title:
        return jsonify({'success': False, 'error': 'Please enter a movie title'})
    
    try:
        rating = int(round(float(rating)))
        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'error': 'Rating must be between 1 and 5'})
    except (ValueError, TypeError):
        return jsonify({'success': False, 'error': 'Invalid rating value'})
    
    try:
        result = rate_movie(title, rating, user_id=session['user_id'], return_movie_id=True)
        
        if not result:
            return jsonify({'success': False, 'error': 'Movie not found in TMDb database'})
        
        # Unpack movie_id, actual_title, and tmdb_rating
        movie_id, actual_title, tmdb_rating = result
        recommendations = []
        
        recs = recommend_similar_movies(movie_id, session['user_id'])
        if recs:
            recommendations = [
                {'title': rec_title, 'rating': rec_rating}
                for _, rec_title, rec_rating in recs
            ]
        
        return jsonify({
            'success': True,
            'movie_title': actual_title,  # Use the actual title from TMDb
            'user_rating': rating,
            'tmdb_rating': tmdb_rating,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/my-movies')
@login_required
def my_movies():
    """API endpoint to get user's rated movies"""
    try:
        rows = get_my_movies(session['user_id'], limit=100)
        
        movies = []
        for title, rating, ts in rows:
            when = ""
            try:
                if ts:
                    dt = _dt.datetime.fromtimestamp(int(ts))
                    when = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass
            
            movies.append({
                'title': title,
                'rating': rating,
                'timestamp': when
            })
        
        return jsonify({'success': True, 'movies': movies})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/movie-details/<path:title>')
@login_required
def movie_details(title):
    """API endpoint to get detailed movie information"""
    import requests
    
    try:
        api_key = os.getenv('TMDB_API_KEY')
        if not api_key:
            return jsonify({'success': False, 'error': 'API key not configured'})
        
        # Search for movie
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        response = requests.get(search_url)
        data = response.json()
        
        if data.get('results'):
            movie = data['results'][0]
            poster_path = movie.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            
            return jsonify({
                'success': True,
                'title': movie.get('title'),
                'overview': movie.get('overview'),
                'poster_url': poster_url,
                'release_date': movie.get('release_date'),
                'rating': movie.get('vote_average'),
                'popularity': movie.get('popularity')
            })
        else:
            return jsonify({'success': False, 'error': 'Movie not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/friends')
@login_required
def friends():
    """API endpoint to get friends list with movie stats"""
    try:
        user_id = session.get('user_id')
        friends_list = get_friends(user_id)
        return jsonify({'success': True, 'friends': friends_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/friends/add', methods=['POST'])
@login_required
def add_friend_route():
    """API endpoint to add a friend"""
    try:
        data = request.get_json()
        friend_username = data.get('username', '').strip()
        
        if not friend_username:
            return jsonify({'success': False, 'error': 'Username is required'})
        
        user_id = session.get('user_id')
        success, message = add_friend(user_id, friend_username)
        
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/trends')
@login_required
def trends():
    """API endpoint to get trending movies from TMDb"""
    try:
        import requests
        
        api_key = os.environ.get('TMDB_API_KEY')
        if not api_key:
            return jsonify({'success': False, 'error': 'TMDb API key not configured'})
        
        # Get trending movies this week
        url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}'
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            movies = []
            
            for movie in data.get('results', [])[:12]:  # Get top 12
                poster_path = movie.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                
                movies.append({
                    'title': movie.get('title', 'Unknown'),
                    'poster_url': poster_url,
                    'rating': round(movie.get('vote_average', 0), 1),
                    'release_date': movie.get('release_date', ''),
                    'overview': movie.get('overview', ''),
                    'popularity': round(movie.get('popularity', 0), 1)
                })
            
            return jsonify({'success': True, 'movies': movies})
        else:
            return jsonify({'success': False, 'error': 'Failed to fetch trending movies'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
