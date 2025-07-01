import tkinter as tk
from tkinter import ttk
from game_data import GAME_DATA

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self._handle_keyrelease)
        self['values'] = self._completion_list

    def _handle_keyrelease(self, event):
        if event.keysym in ("BackSpace", "Left", "Right", "Up", "Down"):
            return

        # Get typed text
        value = self.get()
        value = value.strip().lower()

        # Filter matching items
        if value == '':
            data = self._completion_list
        else:
            data = [item for item in self._completion_list if value in item.lower()]

        self['values'] = data

# Updates role when a character is seleced
def on_character_select(team_list, game_type, row, character):

    if not character == "unknown" and character in GAME_DATA[game_type.get()]['characters']:
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
    row['character'] = AutocompleteCombobox(team_frame, textvariable=row['character_var'])
    row['character'].set_completion_list(GAME_DATA[game_type.get()]['characters'])
    row['role'] = ttk.Combobox(team_frame, textvariable=row['role_var'], values=GAME_DATA[game_type.get()]['roles'], state="readonly")
    current_row = len(team_list) + 1
    row['name'].grid(row=current_row, column=0)
    row['character'].grid(row=current_row, column=1)
    row['role'].grid(row=current_row, column=2)
    team_list.append(row)

    # Run on_character_select whenever a new player is selected
    row['character_var'].trace_add("write", lambda *args: on_character_select(team_list, game_type, team_list.index(row), row['character_var'].get()))

# Function to remove player row
def remove_player_row(team_list):
    index = len(team_list) - 1

    team_list[index]['name'].destroy()
    team_list[index]['character'].destroy()
    team_list[index]['role'].destroy()

    team_list.pop(index)

# Function to remove player row
def clear_player(team_list):
    while(len(team_list) > 0):
        team_list[0]['name'].destroy()
        team_list[0]['character'].destroy()
        team_list[0]['role'].destroy()

        team_list.pop(0)

# Add a new map pick dynamically
def add_map(root, game_type, map_list):
    button = {}
    button['map_var'] = tk.StringVar(value="None")
    col = len(map_list) + 1

    button['map'] = AutocompleteCombobox(root, textvariable=button['map_var'])
    button['map'].set_completion_list(GAME_DATA[game_type.get()]['maps'])
    button['map'].grid(row=5, column=col, padx=5, pady=5)  # Properly place in grid
    map_list.append(button)

def clear_map(map_list):
    while(len(map_list) > 0):
        map_list[0]['map'].destroy()
        map_list.pop(0)

# Add a new ban pick dynamically
def add_ban(root, game_type, ban_list):
    button = {}
    button['ban_var'] = tk.StringVar(value="None")
    col = len(ban_list) + 1

    button['ban'] = AutocompleteCombobox(root, textvariable=button['ban_var'])
    button['ban'].set_completion_list(GAME_DATA[game_type.get()]['characters'])
    button['ban'].grid(row=6, column=col, padx=5, pady=5)  # Properly place in grid
    ban_list.append(button)

def clear_ban(ban_list):
    while(len(ban_list) > 0):
        ban_list[0]['ban'].destroy()
        ban_list.pop(0)
    
# Function to refresh player rows after removal
def refresh_player_rows(team_list):
    for idx, row in enumerate(team_list):
        row['name'].grid(row=idx + 1, column=0)
        row['character'].grid(row=idx + 1, column=1)
        row['role'].grid(row=idx + 1, column=2)

# Update dropdown menus
def update_player_dropdown(row, game_type):
    characters = GAME_DATA[game_type]["characters"]
    indexes = GAME_DATA[game_type]['char_to_role']
    roles = GAME_DATA[game_type]["roles"]

    # Update character dropdown
    row['character'].configure(values=characters)
    row['character_var'].set("unknown")

    # Update role dropdown
    row['role'].configure(values=roles)
    row['role_var'].set("unknown")

# update dropdowns for all players
def update_all_player_dropdowns(team1_list, team2_list, map_list, ban_list, game_type):

    characters = GAME_DATA[game_type]["characters"]
    maps = GAME_DATA[game_type]["maps"]

    # Update players' dropdowns
    for row in team1_list + team2_list:
        update_player_dropdown(row, game_type)

    # Update map dropdowns
    for map_entry in map_list:
        map_entry['map'].configure(values=maps)
        map_entry['map_var'].set("None")

    # Update ban dropdowns
    for ban_entry in ban_list:
        ban_entry['ban'].configure(values=characters)
        ban_entry['ban_var'].set("None")