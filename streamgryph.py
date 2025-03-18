import tkinter as tk
import json
import os
import sys
from tkinter import filedialog
from tkinter import ttk

from player_management import update_all_player_dropdowns, add_player_row, remove_player_row
from player_management import add_map, add_ban
from game_data import GAME_DATA

# --- Functions ---

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def select_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        target_directory.set(folder_selected)
        print(f"Target directory set to: {folder_selected}")

def save_data():
    data = {
        "team1Name": team1_entry.get(),
        "team2Name": team2_entry.get(),
        "score1": int(score1_entry.get() or 0),
        "score2": int(score2_entry.get() or 0),
        "game": game_type.get(),
        "mapPick": [map['map_var'].get() for map in map_list if map['map_var'].get() != "None"],
        "banPick": [ban['ban_var'].get() for ban in ban_list if ban['ban_var'].get() != "None"],
        "team1": collect_player_data(team1_players),
        "team2": collect_player_data(team2_players)
    }

    os.makedirs(target_directory.get(), exist_ok=True)
    file_path = os.path.join(target_directory.get(), "match_data.json")

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Data saved to {file_path}!")
    tk.Label(root, text=f"Data saved to {file_path}").grid(row=7, column=0, padx=10, sticky="w")

def collect_player_data(team_list):
    players = []
    for row in team_list:
        player_data = {
            'name': row['name'].get(),
            'character': row['character_var'].get(),
            'role': row['role_var'].get()
        }
        players.append(player_data)
    return players

# --- Tkinter Window Setup ---
root = tk.Tk()
root.title("StreamGryph - Team Manager")
root.iconbitmap(resource_path('icon.ico'))
root.geometry("900x600")
root.minsize(900, 600)

# Enable window resizing support
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)  # Teams section should grow dynamically

target_directory = tk.StringVar(value="data")
team1_players = []
team2_players = []
ban_list = []
map_list = []
game_type = tk.StringVar(value="Valorant")

# --- Title Section ---
title_label = tk.Label(root, text="StreamGryph Team Manager", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# --- Game Selection Section ---
game_frame = tk.Frame(root)
game_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

# Label + DropDown
tk.Label(game_frame, text="Select Game:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, sticky="w")
game_menu = ttk.Combobox(game_frame, textvariable=game_type, values=list(GAME_DATA.keys()), state="readonly")
game_menu.grid(row=0, column=1, padx=5, sticky="ew")
game_menu.bind("<<ComboboxSelected>>", lambda _: update_all_player_dropdowns(team1_players, team2_players, map_list, ban_list, game_type.get()))

# --- Score and Team Name Section ---
score_frame = tk.LabelFrame(root, text="Match Info")
score_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Labels
tk.Label(score_frame, text="Team 1 Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
tk.Label(score_frame, text="Team 2 Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
tk.Label(score_frame, text="Team 1 Score:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
tk.Label(score_frame, text="Team 2 Score:").grid(row=3, column=0, padx=5, pady=5, sticky="w")

# Text Boxes
team1_entry = tk.Entry(score_frame, width=20)
team2_entry = tk.Entry(score_frame, width=20)
score1_entry = tk.Entry(score_frame, width=5)
score2_entry = tk.Entry(score_frame, width=5)
team1_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
team2_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
score1_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
score2_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# --- Scrollable Team Frames ---
def create_scrollable_frame(parent):
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Use grid() instead of pack()
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Ensure expansion
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    return scroll_frame

# Create the scrollable box for Team 1
team1_frame = tk.LabelFrame(root, text="Team 1")
team1_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
team1_scroll = create_scrollable_frame(team1_frame)

# Create the "Add Player button" (Team 1)
team1_frame.columnconfigure(0, weight=1)
team1_scroll = create_scrollable_frame(team1_frame)
team1_button_frame = tk.Frame(team1_frame)
team1_button_frame.grid(row=1, column=0, pady=5)
tk.Button(team1_button_frame, text="Add Player", command=lambda: add_player_row(team1_scroll, team1_players, game_type)).grid(row=0, column=0, padx=10, pady=5)

# Create the scrollable box for Team 2
team2_frame = tk.LabelFrame(root, text="Team 2")
team2_frame.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
team2_scroll = create_scrollable_frame(team2_frame)

# Create the "Add Player button" (Team 2)
team2_frame.columnconfigure(0, weight=1)
team2_scroll = create_scrollable_frame(team2_frame)
team2_button_frame = tk.Frame(team2_frame)
team2_button_frame.grid(row=1, column=0, pady=5)
tk.Button(team2_button_frame, text="Add Player", command=lambda: add_player_row(team2_scroll, team2_players, game_type)).grid(row=0, column=0, padx=10, pady=5)

# --- Map & Ban Section ---
map_ban_frame = tk.LabelFrame(root, text="Map & Ban Picks")
map_ban_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# A separate frame inside for dynamic elements
map_list_frame = tk.Frame(map_ban_frame)
map_list_frame.grid(row=0, column=1, sticky="w")
ban_list_frame = tk.Frame(map_ban_frame)
ban_list_frame.grid(row=1, column=1, sticky="w")

# Ban and Map Buttons + Frame
tk.Label(map_ban_frame, text="Maps:").grid(row=0, column=0, padx=10, sticky="w")
tk.Label(map_ban_frame, text="Bans:").grid(row=1, column=0, padx=10, sticky="w")
tk.Button(map_ban_frame, text="Add Map", command=lambda: add_map(map_list_frame, game_type, map_list)).grid(row=0, column=2, padx=10, pady=5)
tk.Button(map_ban_frame, text="Add Ban", command=lambda: add_ban(ban_list_frame, game_type, ban_list)).grid(row=1, column=2, padx=10, pady=5)

# --- Save & Directory Section ---
save_frame = tk.Frame(root)
save_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

tk.Label(save_frame, text="Save Directory:").pack(side="left", padx=10)
tk.Label(save_frame, textvariable=target_directory, relief="sunken", width=30).pack(side="left", padx=5)
tk.Button(save_frame, text="Change", command=select_directory).pack(side="left", padx=5)
tk.Button(root, text="Save", command=save_data, font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2, pady=10)

# --- Start Main Loop ---
root.mainloop()