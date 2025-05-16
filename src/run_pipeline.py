import subprocess
import os

def run_script(path):
    subprocess.run(["python", path])

if __name__ == "__main__":
    base = os.path.join("src", "extract")

    run_script(os.path.join(base, "create_tables.py"))
    run_script(os.path.join(base, "insert_data.py"))

    choice = input("Vrei sa adaugi manual un film? (y/n): ").strip().lower()
    if choice == "y":
        run_script(os.path.join(base, "rate_movie.py"))

    run_script(os.path.join("src", "transform", "transformer_pipeline.py"))
    print("Pipeline complet.")
