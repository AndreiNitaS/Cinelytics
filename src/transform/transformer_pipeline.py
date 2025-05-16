import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


from src.extract.db_config import get_connection    


def read_sql(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def execute_query(sql: str) -> None:
    conn = get_connection()
    crs = conn.cursor()

    crs.execute(sql)
    conn.commit()
    print("SQL executed successfully.")
    crs.close()
    conn.close()


if __name__ == "__main__":
    query_paths = [
    os.path.join(BASE_DIR, "tables", "staging", "coolTable_movie_ratings.sql")
]


    for path in query_paths:
        sql_query = read_sql(path)
        execute_query(sql_query)

    from src.extract.populate_staged import populate_coolTable_movie_ratings
    print("coolTable_movie_ratings has been popuated")
    populate_coolTable_movie_ratings()
