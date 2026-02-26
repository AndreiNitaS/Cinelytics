"""
Friends management module for Cinelytics
"""
from extract.db_config import get_connection

def create_friends_table():
    """Create friends table if not exists"""
    sql = """
    CREATE TABLE IF NOT EXISTS friends (
        friendship_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INTEGER NOT NULL,
        friend_id     INTEGER NOT NULL,
        created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(userid),
        FOREIGN KEY (friend_id) REFERENCES users(userid),
        UNIQUE(user_id, friend_id)
    );
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def add_friend(user_id: int, friend_username: str):
    """Add a friend by username. Returns True if successful."""
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Get friend's user_id
        cur.execute("SELECT userid FROM users WHERE username = ?", (friend_username,))
        row = cur.fetchone()
        
        if not row:
            cur.close()
            conn.close()
            return False, "User not found"
        
        friend_id = row[0]
        
        if friend_id == user_id:
            cur.close()
            conn.close()
            return False, "You cannot add yourself as a friend"
        
        # Check if already friends
        cur.execute("SELECT 1 FROM friends WHERE user_id = ? AND friend_id = ?", (user_id, friend_id))
        if cur.fetchone():
            cur.close()
            conn.close()
            return False, "Already friends"
        
        # Add friendship (bidirectional)
        cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (?, ?)", (user_id, friend_id))
        cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (?, ?)", (friend_id, user_id))
        
        conn.commit()
        cur.close()
        conn.close()
        return True, "Friend added successfully"
    except Exception as e:
        cur.close()
        conn.close()
        return False, str(e)

def get_friends(user_id: int):
    """Get all friends for a user with their stats"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT u.userid, u.username, COUNT(r.movieid) as movies_rated
        FROM friends f
        JOIN users u ON f.friend_id = u.userid
        LEFT JOIN userratings r ON u.userid = r.userid
        WHERE f.user_id = ?
        GROUP BY u.userid, u.username
        ORDER BY movies_rated DESC
    """, (user_id,))
    
    friends = []
    colors = [
        'from-blue-400 to-blue-600',
        'from-purple-400 to-purple-600',
        'from-green-400 to-green-600',
        'from-red-400 to-red-600',
        'from-amber-400 to-amber-600',
        'from-pink-400 to-pink-600',
        'from-indigo-400 to-indigo-600',
        'from-cyan-400 to-cyan-600'
    ]
    
    for idx, row in enumerate(cur.fetchall()):
        friend_id, username, movies_rated = row
        initials = ''.join([word[0].upper() for word in username.split()[:2]]) if ' ' in username else username[:2].upper()
        
        # Calculate similarity (placeholder - you can implement proper similarity calculation)
        similarity = 75 + (idx % 20)
        
        friends.append({
            'id': friend_id,
            'username': username,
            'initials': initials,
            'movies_rated': movies_rated,
            'similarity': similarity,
            'color': colors[idx % len(colors)]
        })
    
    cur.close()
    conn.close()
    return friends

# Initialize table
try:
    create_friends_table()
except Exception as e:
    print(f"Warning: Could not initialize friends table: {e}")
