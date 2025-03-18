import tkinter as tk
from tkinter import ttk
from game_data import GAME_DATA

# Updates role when a character is seleced
def on_character_select(team_list, game_type, row, character):

    if not character == "unknown":
        # Find the index of the given character in the game data list
        char_to_index = GAME_DATA[game_type.get()]['characters'].index(character)
        char_to_index = GAME_DATA[game_type.get()]['char_to_role'][char_to_index]
        role = GAME_DATA[game_type.get()]['roles'][char_to_index]

        #Update the role of the player to follow the character
        team_list[row]['role_var'].set(role)

# Function to add player row dynamically
def add_player_row(team_frame, team_list, game_type):
    row = {}
    row['character_var'] = tk.StringVar(value="unknown")
    row['role_var'] = tk.StringVar(value="unknown")
    row['name'] = tk.Entry(team_frame, width=15)
    row['character'] = ttk.Combobox(team_frame, textvariable=row['character_var'], values=GAME_DATA[game_type.get()]['characters'], state="readonly")
    row['role'] = ttk.Combobox(team_frame, textvariable=row['role_var'], values=GAME_DATA[game_type.get()]['roles'], state="readonly")
    current_row = len(team_list) + 1
    row['name'].grid(row=current_row, column=0)
    row['character'].grid(row=current_row, column=1)
    row['role'].grid(row=current_row, column=2)
    team_list.append(row)

    # Run on_character_select whenever a new player is selected
    row['character_var'].trace_add("write", lambda *args: on_character_select(team_list, game_type, team_list.index(row), row['character_var'].get()))

# Add a new map pick dynamically
def add_map(root,game_type,map_list):
    button = {}
    button['map_var'] = tk.StringVar(value="None")
    col = len(map_list) + 1

    button['map'] = ttk.Combobox(root, textvariable=button['map_var'], values=GAME_DATA[game_type.get()]['maps'], state="readonly").grid(row=5,column=col)
    map_list.append(button)

# Add new ban dynamically
def add_ban(root,game_type,ban_list):
    button = {}
    button['ban_var'] = tk.StringVar(value="None")
    col = len(ban_list) + 1

    button['ban'] = ttk.Combobox(root, textvariable=button['ban_var'], values=GAME_DATA[game_type.get()]['characters'], state="readonly").grid(row=6,column=col)
    ban_list.append(button)

# Function to remove player row
def remove_player_row(team_frame, team_list):
    if(team_frame):
        last_row = team_frame[-1];
        for widget in last_row.values():
            widget.grid_forget()
            widget.destroy()
        team_list.pop()
        refresh_player_rows(team_list)
    
    
# Function to refresh player rows after removal
def refresh_player_rows(team_list):
    for idx, row in enumerate(team_list):
        row['name'].grid(row=idx + 1, column=0)
        row['character'].grid(row=idx + 1, column=1)
        row['role'].grid(row=idx + 1, column=2)

# Update dropdown menus
def update_player_dropdown(row, game_type):
    characters = GAME_DATA[game_type]["characters"]
    roles = GAME_DATA[game_type]["roles"]

    # Update character dropdown
    row['character'].configure(values=characters)
    row['character_var'].set(characters[0])

    # Update role dropdown
    row['role'].configure(values=roles)
    row['role_var'].set(roles[0])

# update dropdowns for all players
def update_all_player_dropdowns(team1_list, team2_list, game_type):
    for row in team1_list + team2_list:
        update_player_dropdown(row, game_type)