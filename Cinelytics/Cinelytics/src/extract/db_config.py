import os
import sqlite3
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# This function establishes a connection to the SQLite database.
# SQLite stores data in a single file - no server required!
 
def get_connection():
    # Get the database path - store it in the src directory
    db_path = os.path.join(os.path.dirname(__file__), '..', 'cinelytics.db')
    conn = sqlite3.connect(db_path)
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    return conn