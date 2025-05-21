import tkinter as tk
from tkinter import messagebox
import random
from faker import Faker
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "Cinelytics", "src"))
from extract.db_config import get_connection
from extract.rate_movie import rate_movie
from extract.recommend_movies import recommend_similar_movies

fake = Faker()

def on_submit():
    title = title_entry.get().strip()
    rating = rating_var.get()
    if not title:
        messagebox.showerror("Error", "Please enter a movie title.")
        return

    user_id = random.randint(1000, 9999)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Rating “{title}” as {rating} ⭐ for user {user_id}...\n\n")

    try:
        movie_id = rate_movie(title, rating, user_id=user_id, return_movie_id=True)
        if not movie_id:
            output_text.insert(tk.END, "Movie not found.\n")
            return

        recs = recommend_similar_movies(movie_id, user_id)
        if not recs:
            output_text.insert(tk.END, "No recommendations found.\n")
        else:
            output_text.insert(tk.END, "You might also enjoy:\n")
            for _, rec_title, rec_rating in recs:
                output_text.insert(tk.END, f" • {rec_title} (Rating: {rec_rating})\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("🎬 Cinelytics — Rate & Recommend")

tk.Label(root, text="Movie Title:").pack(padx=10, pady=(10, 0))
title_entry = tk.Entry(root, width=40)
title_entry.pack(padx=10, pady=(0, 10))

tk.Label(root, text="Your Rating (1–5):").pack()
rating_var = tk.IntVar(value=3)
tk.OptionMenu(root, rating_var, *range(1, 6)).pack(padx=10, pady=(0, 10))

tk.Button(root, text="Submit", command=on_submit).pack(pady=(0, 10))

output_text = tk.Text(root, width=60, height=15)
output_text.pack(padx=10, pady=(0, 10))

root.mainloop()
