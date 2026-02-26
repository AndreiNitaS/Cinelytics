from extract.db_config import get_connection

def get_my_movies(user_id: int, limit: int = 50):
    """
    Returns a list of (title, rating, rated_at_ts) for this user,
    newest first. 'rated_at_ts' is a Unix timestamp (BIGINT) in your raw.userratings.
    """
    sql = """
    SELECT m.title,
           r.rating,
           r.rating_ts
    FROM userratings r
    JOIN moviemetadata m ON m.movieid = r.movieid
    WHERE r.userid = ?
    ORDER BY r.rating_ts DESC
    LIMIT ?;
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (user_id, limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
