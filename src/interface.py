import tkinter as tk
from tkinter import messagebox, ttk
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
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Rating “{title}” as {rating} ⭐ for user {user_id}...\n\n")

    try:
        result = rate_movie(title, rating, user_id=user_id, return_movie_id=True)
        if not result:
            output_text.insert(tk.END, "Movie not found.\n")
            return
        
        movie_id, imdb_rating = result
        output_text.insert(tk.END, f"IMDb Rating: {imdb_rating} ⭐\n\n")


        recs = recommend_similar_movies(movie_id, user_id)
        if not recs:
            output_text.insert(tk.END, "No recommendations found.\n")
        else:
            output_text.insert(tk.END, "🎯 You might also enjoy:\n\n")
            for _, rec_title, rec_rating in recs:
                output_text.insert(tk.END, f" • {rec_title}  ⭐ {rec_rating}\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    output_text.config(state="disabled")

root = tk.Tk()
root.title("🎬 Cinelytics — Rate & Recommend")
root.geometry("600x450")
root.resizable(False, False)

main_font = ("Segoe UI", 11)
label_font = ("Segoe UI", 10, "bold")

tk.Label(root, text="Movie Title:", font=label_font).pack(anchor="w", padx=15, pady=(15, 0))
title_entry = tk.Entry(root, width=45, font=main_font)
title_entry.pack(padx=15, pady=(0, 10))

tk.Label(root, text="Your Rating (1–5):", font=label_font).pack(anchor="w", padx=15)
rating_var = tk.IntVar(value=3)
tk.Scale(root, from_=1, to=5, orient="horizontal", variable=rating_var, showvalue=True, resolution=1, length=200).pack(padx=15, pady=(0, 10))


tk.Button(root, text="Submit", command=on_submit, font=main_font).pack(pady=(0, 15))

output_frame = tk.Frame(root, borderwidth=1, relief="sunken")
output_frame.pack(padx=15, pady=(0, 15), fill="both", expand=True)

output_text = tk.Text(output_frame, wrap="word", font=("Consolas", 10), background="#f9f9f9")
output_text.pack(fill="both", expand=True, padx=5, pady=5)
output_text.config(state="disabled")

root.mainloop()