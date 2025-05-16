import subprocess
import os

# This script runs the entire ETL pipeline for the Cinelytics project.
# It executes the following steps:
## 1. Create tables in the PostgreSQL database.
## 2. Insert data into the tables.
## 3. Optionally, allow the user to manually add a movie.
## 4. Transform the data using a transformer pipeline.
## 5. Print a message indicating that the pipeline is complete.


import subprocess
import os

def run_script(path):
    subprocess.run(["python", path])

if __name__ == "__main__":
    base_extract = os.path.join("src", "extract")
    base_transform = os.path.join("src", "transform")

    run_script(os.path.join(base_extract, "create_tables.py"))
    run_script(os.path.join(base_extract, "insert_data.py"))

    while True:
        choice = input("Do you want to add a new movie? (y/n): ").strip().lower()
        if choice == "y":
            run_script(os.path.join(base_extract, "rate_movie.py"))
        else:
            break

    run_script(os.path.join(base_transform, "transformer_pipeline.py"))
    run_script(os.path.join(base_transform, "populate_movie_reception.py"))

    print("Pipeline complet.")

