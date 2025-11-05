import os
from dotenv import load_dotenv, find_dotenv
import psycopg2

load_dotenv(find_dotenv())
# This function establishes a connection to the PostgreSQL database using the credentials
# stored in environment variables. It returns a connection object that can be used to interact
# with the database.
 
def get_connection():
    return psycopg2.connect(
        host     = os.getenv("DB_HOST"),
        port     = os.getenv("DB_PORT"),
        dbname   = os.getenv("DB_NAME"),
        user     = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )