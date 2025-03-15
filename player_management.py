import tkinter as tk
from game_data import GAME_DATA

# Function to add player row dynamically
def add_player_row(team_frame, team_list, game_type):
    row = {}
    row['character_var'] = tk.StringVar(value="unknown")
    row['role_var'] = tk.StringVar(value="unknown")
    row['name'] = tk.Entry(team_frame, width=15)
    row['character'] = tk.OptionMenu(team_frame, row['character_var'], *GAME_DATA[game_type.get()]['characters'])
    row['role'] = tk.OptionMenu(team_frame, row['role_var'], *GAME_DATA[game_type.get()]['roles'])
    current_row = len(team_list) + 1
    row['name'].grid(row=current_row, column=0)
    row['character'].grid(row=current_row, column=1)
    row['role'].grid(row=current_row, column=2)
    team_list.append(row)

# Function to remove player row
def remove_player_row(row, team_list):
    for widget in row.values():
        widget.grid_forget()
        widget.destroy()
    team_list.remove(row)
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
    menu = row['character']['menu']
    menu.delete(0, 'end')
    for char in characters:
        menu.add_command(label=char, command=lambda value=char: row['character_var'].set(value))
    row['character_var'].set(characters[0])

    # Update role dropdown
    menu = row['role']['menu']
    menu.delete(0, 'end')
    for role in roles:
        menu.add_command(label=role, command=lambda value=role: row['role_var'].set(value))
    row['role_var'].set(roles[0])

# update dropdowns for all players
def update_all_player_dropdowns(team1_list, team2_list, game_type):
    for row in team1_list + team2_list:
        update_player_dropdown(row, game_type)