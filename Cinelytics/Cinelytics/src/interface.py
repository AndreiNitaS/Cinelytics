#packages
import os, sys, math
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import datetime as _dt
from faker import Faker
sys.path.append(os.path.join(os.path.dirname(__file__), "Cinelytics", "src"))
from extract.rate_movie import rate_movie
from extract.recommend_movies import recommend_similar_movies
from extract.auth import create_users_table, create_user, authenticate
from extract.my_movies import get_my_movies
from PIL import Image, ImageTk



fake = Faker()
current_user_id = None
current_username = None


#Utils
def center_window(win, w, h):
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - w) // 2, (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

def set_status(msg):
    status_var.set(msg)
    status_bar.update_idletasks()




#Authentication functions
def do_login():
    global current_user_id, current_username
    u, p = entry_user.get().strip(), entry_pass.get().strip()
    if not u or not p:
        messagebox.showerror("Error", "Please enter username and password.")
        return
    try:
        uid = authenticate(u, p)
    except Exception as e:
        messagebox.showerror("DB Error", str(e))
        return
    if uid is None:
        messagebox.showerror("Login failed", "Invalid username or password.")
        return
    current_user_id, current_username = uid, u
    messagebox.showinfo("Welcome", f"Logged in as {u}")
    set_status(f"Logged in as {u}")
    refresh_session_box()
    show_app_frame()

def do_signup():
    u, p = entry_user.get().strip(), entry_pass.get().strip()
    if not u or not p:
        messagebox.showerror("Error", "Please enter username and password.")
        return
    try:
        create_user(u, p)
        messagebox.showinfo("Success", "Account created. You can now log in.")
        set_status("Account created.")
    except Exception as e:
        messagebox.showerror("Sign up failed", str(e))

def refresh_session_box():
    if current_user_id is None:
        session_box.config(state="normal")
        session_box.delete("1.0", tk.END)
        session_box.insert("1.0", "Login to start rating.")
        session_box.config(state="disabled")
    else:
        session_box.config(state="normal")
        session_box.delete("1.0", tk.END)
        session_box.insert("1.0", f"Logged in as {current_username}")
        session_box.config(state="disabled")


def do_logout():
    global current_user_id, current_username
    current_user_id, current_username = None, None
    title_entry.delete(0, tk.END)
    rating_var.set(3.0)
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")
    refresh_session_box()
    show_login_frame()
    set_status("Logged out")


#Error handling and movie rating
def on_submit():
    if current_user_id is None:
        messagebox.showerror("Error", "Please log in first.")
        return
    title, rating = title_entry.get().strip(), int(round(float(rating_var.get())))
    if not title:
        messagebox.showerror("Error", "Please enter a movie title.")
        return

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Rating “{title}” as {rating} ⭐...\n\n")

    try:
        result = rate_movie(title, rating, user_id=current_user_id, return_movie_id=True)
        if not result:
            output_text.insert(tk.END, "Movie not found.\n")
            set_status("Movie not found.")
        else:
            movie_id, tmdb_rating = result
            output_text.insert(tk.END, f"TMDb Rating: {tmdb_rating} ⭐\n\n")
            recs = recommend_similar_movies(movie_id, current_user_id)
            if recs:
                output_text.insert(tk.END, "You might also enjoy:\n\n")
                for _, rec_title, rec_rating in recs:
                    output_text.insert(tk.END, f" • {rec_title}  ⭐ {rec_rating}\n")
                set_status("Rated successfully.")
            else:
                output_text.insert(tk.END, "No recommendations found.\n")
                set_status("Rated.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        set_status("Error during rating.")
    output_text.config(state="disabled")

def on_show_my_movies():
    if current_user_id is None:
        messagebox.showerror("Error", "Please log in first.")
        return
    try:
        rows = get_my_movies(current_user_id, limit=100)
    except Exception as e:
        messagebox.showerror("DB Error", str(e))
        return

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    if not rows:
        output_text.insert(tk.END, "You haven't rated any movies yet.\n")
        set_status("No movies yet.")
    else:
        output_text.insert(tk.END, f"🎟️ Your last {len(rows)} rated movies:\n\n")
        for title, rating, ts in rows:
            when = ""
            try:
                if ts:
                    dt = _dt.datetime.fromtimestamp(int(ts))
                    when = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                pass
            output_text.insert(tk.END, f" • {title}  —  ⭐ {rating}  ({when})\n")
        set_status("Loaded your movies.")
    output_text.config(state="disabled")


#Weighted rating bar
def draw_rating_bar(angle_deg):
    """Redraw the rating bar at a given tilt angle and knob position."""
    rating_canvas.delete("all")

    w, h = 260, 60
    cx, cy = w / 2, h / 2 + 2
    length = 210  
    angle = math.radians(angle_deg)


    x1 = cx - math.cos(angle) * length / 2
    y1 = cy - math.sin(angle) * length / 2
    x2 = cx + math.cos(angle) * length / 2
    y2 = cy + math.sin(angle) * length / 2

   
    shadow_offset = 2
    rating_canvas.create_line(
        x1 + shadow_offset, y1 + shadow_offset, x2 + shadow_offset, y2 + shadow_offset,
        width=8, capstyle="round", fill="#d2d5db"
    )
    rating_canvas.create_line(
        x1, y1, x2, y2,
        width=8, capstyle="round", fill=ACCENT
    )

    val = float(rating_var.get())
    t = (val - 1) / 4  
    kx = x1 + (x2 - x1) * t
    ky = y1 + (y2 - y1) * t

    rating_canvas.create_oval(
        kx - 7, ky - 7, kx + 7, ky + 7,
        fill="#ffffff", outline=ACCENT, width=2
    )

def tilt_rating_bar(val):
    """Map value (1..5) to angle (−45..+45) and redraw."""
    try:
        v = float(val)
    except Exception:
        v = 3.0
    angle = (v - 3.0) * 45.0 / 2.0 
    draw_rating_bar(angle)
  

def rating_click_or_drag(event):
    """Click/drag on canvas to set value and tilt bar."""
    w = 260
    x = max(10, min(w - 10, event.x))
    t = (x - 10) / (w - 20)  
    val = 1.0 + t * 4.0
    rating_var.set(val)
    tilt_rating_bar(val)

def rating_key(event):
    step = 0.2
    v = float(rating_var.get())
    if event.keysym in ("Left", "Down"):
        v = max(1.0, v - step)
    elif event.keysym in ("Right", "Up"):
        v = min(5.0, v + step)
    rating_var.set(v)
    tilt_rating_bar(v)


#Frame switching


def show_app_frame():
    login_wrap.pack_forget()
    app_wrap.pack(fill="both", expand=True)
  
    

def show_login_frame():
    app_wrap.pack_forget()
    login_wrap.pack(fill="both", expand=True)
  


#UI Setup
root = tk.Tk()
root.title("Cinelytics")
center_window(root, 820, 640)
root.configure(bg="#f5f5f7")
# Colors
BG      = "#f5f5f7"
CARD    = "#ffffff"
TEXT    = "#111111"
SUBTLE  = "#6b7280"
ACCENT  = "#007aff"   #


BASE_FONT = ("SF Pro Display", 10) if "SF Pro Display" in tkfont.families() else ("Segoe UI", 10)

style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass
style.configure(".", font=BASE_FONT)
style.configure("TFrame", background=BG)
style.configure("Card.TFrame", background=CARD)
style.configure("TLabel", background=CARD, foreground=TEXT)
style.configure("Header.TLabel", background=BG, foreground=TEXT, font=(BASE_FONT[0], 18, "bold"))
style.configure("Sub.TLabel", background=BG, foreground=SUBTLE, font=(BASE_FONT[0], 10))



# Buttons 
def pill_button(master, text, command=None, color=ACCENT):
    btn = tk.Label(master, text=text, bg=color, fg="white",
                   font=(BASE_FONT[0], 10, "bold"),
                   padx=18, pady=6, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="#0a84ff"))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    if command:
        btn.bind("<Button-1>", lambda e: command())
    btn.pack(side="left", padx=6)
    return btn

# Header
header = ttk.Frame(root)
header.pack(fill="x", padx=20, pady=(18, 6))
ttk.Label(header, text="Cinelytics", style="Header.TLabel").pack(side="left")
ttk.Label(header, text="My Little License", style="Sub.TLabel").pack(side="left", padx=(10, 0))

#Login
login_wrap = ttk.Frame(root, style="TFrame")
login_card = ttk.Frame(login_wrap, style="Card.TFrame")
login_card.pack(padx=20, pady=24, fill="x")

tk.Label(login_card, text="Sign In", bg=CARD, fg=TEXT, font=(BASE_FONT[0], 13, "bold")).pack(anchor="w", padx=16, pady=(14, 8))
tk.Label(login_card, text="Username", bg=CARD, fg=SUBTLE).pack(anchor="w", padx=16)
entry_user = tk.Entry(login_card, width=32, relief="flat", highlightthickness=1, highlightcolor=ACCENT)
entry_user.pack(padx=16, pady=(0, 10))
tk.Label(login_card, text="Password", bg=CARD, fg=SUBTLE).pack(anchor="w", padx=16)
entry_pass = tk.Entry(login_card, width=32, show="•", relief="flat", highlightthickness=1, highlightcolor=ACCENT)
entry_pass.pack(padx=16, pady=(0, 10))

login_btns = tk.Frame(login_card, bg=CARD)
login_btns.pack(pady=(8, 14))
pill_button(login_btns, "Log In", do_login, color=ACCENT)
pill_button(login_btns, "Sign Up", do_signup, color="#34c759")

login_wrap.pack(fill="both", expand=True)

# App
app_wrap = ttk.Frame(root, style="TFrame")

top_card = ttk.Frame(app_wrap, style="Card.TFrame")
top_card.pack(fill="x", padx=20, pady=(16, 10))

left = ttk.Frame(top_card, style="Card.TFrame")
left.pack(side="left", fill="both", expand=True, padx=(14, 8), pady=14)

tk.Label(left, text="Movie Title", bg=CARD, fg="#333").pack(anchor="w")
title_entry = tk.Entry(left, width=44, relief="flat", highlightthickness=1, highlightcolor=ACCENT)
title_entry.pack(fill="x", pady=(2, 10))

tk.Label(left, text="Your Rating (1–5)", bg=CARD, fg="#333").pack(anchor="w", pady=(4, 0))

rating_container = tk.Frame(left, bg=CARD, height=70)
rating_container.pack(fill="x", pady=(2, 12))

rating_var = tk.DoubleVar(value=3.0)
rating_canvas = tk.Canvas(rating_container, bg=CARD, bd=0, highlightthickness=0, width=260, height=60)
rating_canvas.pack(pady=6)

# Mouse & keyboard interactions
rating_canvas.bind("<Button-1>", rating_click_or_drag)
rating_canvas.bind("<B1-Motion>", rating_click_or_drag)
root.bind("<Left>", rating_key)
root.bind("<Right>", rating_key)
root.bind("<Up>", rating_key)
root.bind("<Down>", rating_key)

btn_row = tk.Frame(left, bg=CARD)
btn_row.pack(anchor="w", pady=(2, 0))
pill_button(btn_row, "Submit", on_submit, color=ACCENT)
pill_button(btn_row, "My Movies", on_show_my_movies, color="#5856d6")
pill_button(btn_row, "Logout", do_logout, color="#ff3b30")

right = ttk.Frame(top_card, style="Card.TFrame")
right.pack(side="left", fill="both", expand=True, padx=(8, 14), pady=14)

tk.Label(right, text="Session", bg=CARD, fg="#333").pack(anchor="w")
session_box = tk.Text(right, height=5, bg=BG, relief="flat", bd=0)
session_box.pack(fill="both", expand=True, pady=(4, 0))
session_box.insert("1.0", "Login to start rating.\n")
session_box.config(state="disabled")

# Output
output_card = ttk.Frame(app_wrap, style="Card.TFrame")
output_card.pack(fill="both", expand=True, padx=20, pady=(6, 18))
tk.Label(output_card, text="Output", bg=CARD, fg=TEXT, font=(BASE_FONT[0], 12, "bold")).pack(anchor="w", padx=16, pady=(12, 6))
output_text = tk.Text(output_card, wrap="word", font=(BASE_FONT[0], 10), bg="#fbfbfd", relief="flat")
output_text.pack(fill="both", expand=True, padx=16, pady=(0, 16))
output_text.config(state="disabled")

# Status bar
status_var = tk.StringVar(value="Ready")
status_bar = tk.Label(root, textvariable=status_var, bg=BG, fg=SUBTLE, anchor="w", font=(BASE_FONT[0], 9))
status_bar.pack(fill="x", padx=20, pady=(0, 10))

# Ensure DB table exists
try:
    create_users_table()
except Exception as e:
    messagebox.showerror("DB Error", str(e))

# Start on login view
show_login_frame()
set_status("Please log in or sign up.")
tilt_rating_bar(rating_var.get())  

root.mainloop()
