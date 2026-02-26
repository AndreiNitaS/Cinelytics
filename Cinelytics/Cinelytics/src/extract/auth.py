#This is the authentication module for user management in the Cinelytics platform.
import bcrypt
from extract.db_config import get_connection

def create_users_table():
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        userid        INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at    TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def create_user(username: str, password: str) -> int:
    """Creates a user and returns userid. Raises on duplicate username."""
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, pw_hash)
    )
    user_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def authenticate(username: str, password: str):
    """Returns userid if credentials are valid, else None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT userid, password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None
    user_id, pw_hash = row
    ok = bcrypt.checkpw(password.encode("utf-8"), pw_hash.encode("utf-8"))
    return user_id if ok else None
