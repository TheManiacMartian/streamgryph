import tkinter as tk
import json
import os
import sys
from tkinter import filedialog

from player_management import update_all_player_dropdowns, add_player_row, remove_player_row
from game_data import GAME_DATA

# functions

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def select_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        target_directory.set(folder_selected)  # Update target directory
        print(f"Target directory set to: {folder_selected}")

# -- JSON STUFF --

# save JSON data to target directory (TODO: target directory)
def save_data():
    data = {
        "team1Name": team1_entry.get(),
        "team2Name": team2_entry.get(),
        "score1": int(score1_entry.get() or 0),
        "score2": int(score2_entry.get() or 0),
        "game": game_type.get(),
        "team1": [collect_player_data(team1_players)],
        "team2": [collect_player_data(team2_players)]
    }
    
    os.makedirs(target_directory.get(), exist_ok=True)  # Make sure directory exists
    
    file_path = os.path.join(target_directory.get(), "match_data.json")
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Data saved to {file_path}!")

# returns the players in a JSON format
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


# Ensure data folder exists
os.makedirs("data", exist_ok=True)

root = tk.Tk()
root.title("StreamGryph")
root.iconbitmap(resource_path("icon.ico"))

target_directory = tk.StringVar(value="data")

WIDTH = 1000
HEIGHT = 500

x = int((root.winfo_screenwidth() / 2) - (WIDTH / 2))
y = int((root.winfo_screenheight() / 2) - (HEIGHT / 2))

root.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')


team1_players = []
team2_players = []

game_type = tk.StringVar(value="Valorant")



# -- GUI LAYOUT --

# team and score entries
team1_entry = tk.Entry(root)
team2_entry = tk.Entry(root)
score1_entry = tk.Entry(root)
score2_entry = tk.Entry(root)
game_menu = tk.OptionMenu(root, game_type, *GAME_DATA.keys(), command=lambda _: update_all_player_dropdowns(team1_players, team2_players, game_type.get()))

tk.Label(root, text="Team 1 Name:").grid(row=0, column=0)
tk.Label(root, text="Team 2 Name:").grid(row=1, column=0)
tk.Label(root, text="Team 1 Score:").grid(row=2, column=0)
tk.Label(root, text="Team 2 Score:").grid(row=3, column=0)
tk.Label(root, text="Game:").grid(row=4, column=0)

# position them
team1_entry.grid(row=0, column=1)
team2_entry.grid(row=1, column=1)
score1_entry.grid(row=2, column=1)
score2_entry.grid(row=3, column=1)
game_menu.grid(row=4, column=1)

# Teams UI
team1_frame = tk.LabelFrame(root, text="Team 1")
team1_frame.grid(row=5, column=0, padx=10, pady=10)

team2_frame = tk.LabelFrame(root, text="Team 2")
team2_frame.grid(row=5, column=1, padx=10, pady=10)

# Table headers
tk.Label(team1_frame, text="Name").grid(row=0, column=0)
tk.Label(team1_frame, text="Character").grid(row=0, column=1)
tk.Label(team1_frame, text="Role").grid(row=0, column=2)
                                        
tk.Label(team2_frame, text="Name").grid(row=0, column=0)
tk.Label(team2_frame, text="Character").grid(row=0, column=1)
tk.Label(team2_frame, text="Role").grid(row=0, column=2)

tk.Button(team1_frame, text="Add Player", command=lambda: add_player_row(team1_frame, team1_players, game_type)).grid(row=999, column=0, columnspan=1, pady=5)
tk.Button(team2_frame, text="Add Player", command=lambda: add_player_row(team2_frame, team2_players, game_type)).grid(row=999, column=0, columnspan=1, pady=5)

# tk.Button(team1_frame, text="Remove Player", command=lambda: remove_player_row(team1_frame, team1_players)).grid(row=999, column=1, columnspan=1, pady=5)
# tk.Button(team2_frame, text="Remove Player", command=lambda: remove_player_row(team2_frame, team2_players)).grid(row=999, column=1, columnspan=1, pady=5)


# Show current target directory
tk.Label(root, textvariable=target_directory).grid(row=6,column=0,pady=5)

# Button to select target directory
tk.Button(root, text="Select Save Directory", command=select_directory).grid(row=7, column=0, pady=5)

# Save button
tk.Button(root, text="Save", command=save_data).grid(row=8, column=0, columnspan=2, pady=10)

# Status Label
status_label = tk.Label(root, text="")
status_label.grid(row=9, column=0, columnspan=2)

add_player_row(team1_frame, team1_players, game_type)
add_player_row(team2_frame, team2_players, game_type)

root.mainloop()