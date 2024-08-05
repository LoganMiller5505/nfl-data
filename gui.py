import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Load the data with error handling
def load_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {filepath}")
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", f"No data in file: {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data from {filepath}: {e}")
    return pd.DataFrame()

# Load data
qb_results = load_data('final_data/qb_final_predictions.csv')
rb_results = load_data('final_data/rb_final_predictions.csv')
wr_results = load_data('final_data/wr_final_predictions.csv')
te_results = load_data('final_data/te_final_predictions.csv')
adp_rankings = load_data('final_data/FantasyPros_2024_Overall_ADP_Rankings.csv')

# Combine data
for df in [qb_results, rb_results, wr_results, te_results]:
    df['ADP Rank'] = df['display_name'].map(adp_rankings.set_index('Player')['Rank'])
    df['ESPN'] = df['display_name'].map(adp_rankings.set_index('Player')['ESPN'])

# Initialize application
class FantasyFootballApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Fantasy Football Predictions')

        # Initialize variables
        self.drafted_players = { 'QB': [], 'RB': [], 'WR': [], 'TE': [], 'FLEX': [], 'BENCH': [] }
        self.drafted_counts = { 'QB': 0, 'RB': 0, 'WR': 0, 'TE': 0, 'FLEX': 0, 'BENCH': 0 }
        self.struck_players = set()
        self.current_draft_pick = 0  # Initialize draft pick counter

        # Create the main layout
        self.create_search_and_sort()

        # Create the main layout
        self.create_tabs()

    def create_search_and_sort(self):
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill='x')
        
        search_label = ttk.Label(search_frame, text='Search Player:')
        search_label.pack(side='left', padx=5, pady=5)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        
        search_button = ttk.Button(search_frame, text='Search', command=self.refresh_all_frames)
        search_button.pack(side='left', padx=5, pady=5)

        # Create sorting dropdown
        sort_label = ttk.Label(search_frame, text='Sort By:')
        sort_label.pack(side='left', padx=5, pady=5)
        
        self.sort_var = tk.StringVar(value='Fantasy Points')
        self.sort_dropdown = ttk.Combobox(search_frame, textvariable=self.sort_var, values=['Fantasy Points', 'ADP Rank', 'ESPN'])
        self.sort_dropdown.pack(side='left', padx=5, pady=5)
        self.sort_dropdown.bind("<<ComboboxSelected>>", lambda event: self.refresh_all_frames())

        # Current Draft Pick Counter
        self.draft_pick_label = ttk.Label(search_frame, text=f'Current Draft Pick: {self.current_draft_pick}', font=('Helvetica', 12))
        self.draft_pick_label.pack(side='left', padx=10, pady=5)

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        self.frame_widgets = {}
        self.frames = {
            'Quarterbacks': qb_results,
            'Running Backs': rb_results,
            'Wide Receivers': wr_results,
            'Tight Ends': te_results,
            'All Players': pd.concat([qb_results, rb_results, wr_results, te_results]).sort_values(by='fantasy_points', ascending=False),
            'Drafted Players': pd.DataFrame(columns=['display_name', 'fantasy_points', 'ADP Rank', 'ESPN'])  # Initially empty
        }

        for tab_name, data in self.frames.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.frame_widgets[tab_name] = frame
            if tab_name == 'Drafted Players':
                self.create_drafted_section(frame)
            else:
                self.display_predictions(frame, data)

    def create_drafted_section(self, frame):
        ttk.Label(frame, text='Drafted Players', font=('Helvetica', 12, 'bold')).pack(pady=5)

        # Create sections for each position
        self.position_frames = {}
        for position in ['QB', 'RB', 'WR', 'TE', 'FLEX', 'BENCH']:
            position_frame = ttk.LabelFrame(frame, text=position, padding=(10, 5))
            position_frame.pack(pady=5, fill='x')

            # Add a Treeview for each position
            tree = self.create_treeview(position_frame)
            self.position_frames[position] = tree

    def create_treeview(self, parent_frame):
        tree = ttk.Treeview(parent_frame, columns=('display_name', 'fantasy_points', 'ADP Rank', 'ESPN'), show='headings', height=5)
        tree.pack(expand=True, fill='both')
        tree.heading('display_name', text='Player')
        tree.heading('fantasy_points', text='Fantasy Points')
        tree.heading('ADP Rank', text='ADP Rank')
        tree.heading('ESPN', text='ESPN')
        return tree

    def refresh_all_frames(self):
        for tab_name, data in self.frames.items():
            if tab_name == 'Drafted Players':
                self.refresh_drafted_section()
            else:
                # Sort results based on selected criteria
                sort_key = self.sort_var.get()
                if sort_key == 'ADP Rank':
                    data = data.sort_values(by='ADP Rank', ascending=True)
                elif sort_key == 'ESPN':
                    data = data.sort_values(by='ESPN', ascending=True)
                else:  # Default to sorting by fantasy points
                    data = data.sort_values(by='fantasy_points', ascending=False)
                
                self.display_predictions(self.frame_widgets[tab_name], data)

    def display_predictions(self, frame, results):
        # Clear existing treeview if any
        for widget in frame.winfo_children():
            widget.destroy()

        # Filter results based on search query
        search_query = self.search_entry.get()
        if search_query:
            results = results[results['display_name'].str.contains(search_query, case=False, na=False)]

        tree = self.create_treeview(frame)

        # Insert data with strikethrough and green color where applicable
        for _, row in results.iterrows():
            player_name = row['display_name']
            fantasy_points = row['fantasy_points']
            adp_rank = row.get('ADP Rank', 'N/A')  # Handle missing ADP Rank
            espn = row.get('ESPN', 'N/A')          # Handle missing ESPN

            tags = []

            if player_name in self.struck_players:
                tags.append('struck')
            if player_name in self.get_all_drafted_players():
                tags.append('drafted')

            tree.insert('', 'end', text=player_name, values=(player_name, fantasy_points, adp_rank, espn), tags=tags)

        # Add tag configuration for strikethrough and green color
        tree.tag_configure('struck', font=('Helvetica', 10, 'overstrike'))
        tree.tag_configure('drafted', background='lightgreen')

        # Bind the click event to toggle strikethrough and context menu
        tree.bind('<Double-1>', self.toggle_strikethrough)
        tree.bind('<Button-3>', lambda event: self.show_context_menu(event, tree, results))

    def toggle_strikethrough(self, event):
        item = event.widget.selection()[0]
        player_name = event.widget.item(item, 'text')

        # Do not allow strikethrough for players in "Drafted Players"
        if player_name in self.get_all_drafted_players():
            return

        if player_name in self.struck_players:
            self.struck_players.remove(player_name)
            self.current_draft_pick -= 1  # Decrement counter when strikethrough is removed
        else:
            self.struck_players.add(player_name)
            self.current_draft_pick += 1  # Increment counter when a player is struck through

        # Refresh all frames to update styles
        self.refresh_all_frames()
        self.update_draft_pick_label()  # Update the draft pick counter label

    def get_all_drafted_players(self):
        return [player['display_name'] for position in self.drafted_players.values() for player in position]

    def add_to_drafted(self, player_data):
        player_dict = player_data.to_dict()  # Convert player_data to dictionary
        position = player_dict['position']
        
        # Create a new player dictionary to ensure all keys are present
        drafted_player_dict = {
            'display_name': player_dict['display_name'],
            'fantasy_points': player_dict['fantasy_points'],
            'ADP Rank': player_dict.get('ADP Rank', 'N/A'),  # Use 'N/A' if 'Rank' is missing
            'ESPN': player_dict.get('ESPN', 'N/A'),          # Use 'N/A' if 'ESPN' is missing
            'position': position
        }

        # Add player to drafted counts with limits
        if position == 'QB' and self.drafted_counts['QB'] < 1:
            self.drafted_counts['QB'] += 1
            self.drafted_players['QB'].append(drafted_player_dict)
            self.current_draft_pick += 1  # Increment counter when player is drafted
        elif position == 'RB' and self.drafted_counts['RB'] < 2:
            self.drafted_counts['RB'] += 1
            self.drafted_players['RB'].append(drafted_player_dict)
            self.current_draft_pick += 1
        elif position == 'WR' and self.drafted_counts['WR'] < 2:
            self.drafted_counts['WR'] += 1
            self.drafted_players['WR'].append(drafted_player_dict)
            self.current_draft_pick += 1
        elif position == 'TE' and self.drafted_counts['TE'] < 1:
            self.drafted_counts['TE'] += 1
            self.drafted_players['TE'].append(drafted_player_dict)
            self.current_draft_pick += 1
        elif position in ['RB', 'WR', 'TE'] and self.drafted_counts['FLEX'] < 1:
            self.drafted_counts['FLEX'] += 1
            drafted_player_dict['position'] = 'FLEX'  # Explicitly set position to FLEX
            self.drafted_players['FLEX'].append(drafted_player_dict)
            self.current_draft_pick += 1
        elif self.drafted_counts['BENCH'] < 7:
            self.drafted_counts['BENCH'] += 1
            drafted_player_dict['position'] = 'BENCH'  # Explicitly set position to BENCH
            self.drafted_players['BENCH'].append(drafted_player_dict)
            self.current_draft_pick += 1
        else:
            return  # Limit reached; do not add player

        self.refresh_all_frames()  # Refresh all frames to update drafted players
        self.update_draft_pick_label()  # Update the draft pick counter label

    def remove_from_drafted(self, player_data):
        player_dict = player_data.to_dict()  # Convert player_data to dictionary

        for pos in self.drafted_players:
            player_dict['position'] = pos
            if player_dict in self.drafted_players[pos]:
                self.drafted_players[pos].remove(player_dict)
                
                # Decrement the appropriate count
                if pos == 'QB':
                    self.drafted_counts['QB'] -= 1
                elif pos == 'RB':
                    self.drafted_counts['RB'] -= 1
                elif pos == 'WR':
                    self.drafted_counts['WR'] -= 1
                elif pos == 'TE':
                    self.drafted_counts['TE'] -= 1
                elif pos == 'FLEX':
                    self.drafted_counts['FLEX'] -= 1
                elif pos == 'BENCH':
                    self.drafted_counts['BENCH'] -= 1
                
                self.current_draft_pick -= 1  # Decrement counter when a player is removed
                break

        self.refresh_all_frames()  # Refresh all frames to update drafted players
        self.update_draft_pick_label()  # Update the draft pick counter label

    def show_context_menu(self, event, tree, results):
        item = tree.identify_row(event.y)
        if item:
            player_name = tree.item(item, 'text')
            player_data = results[results['display_name'] == player_name].iloc[0]

            context_menu = tk.Menu(self.root, tearoff=0)
            if player_name in self.get_all_drafted_players():
                context_menu.add_command(label="Remove from Drafted", command=lambda: self.remove_from_drafted(player_data))
            elif player_name not in self.struck_players:
                context_menu.add_command(label="Add to Drafted", command=lambda: self.add_to_drafted(player_data))
            context_menu.post(event.x_root, event.y_root)

    def refresh_drafted_section(self):
        for position, players in self.drafted_players.items():
            tree = self.position_frames[position]
            if tree.winfo_exists():  # Check if the widget exists before deleting its children
                tree.delete(*tree.get_children())  # Clear existing items

                # Insert drafted players into the treeview by position
                for player in players:
                    tree.insert('', 'end', text=player['display_name'], values=(player['display_name'], player['fantasy_points'], player['ADP Rank'], player['ESPN']))

    def update_draft_pick_label(self):
        self.draft_pick_label.config(text=f'Current Draft Pick: {self.current_draft_pick}')  # Update label with current count

# Start the main event loop
if __name__ == "__main__":
    root = tk.Tk()
    app = FantasyFootballApp(root)
    root.mainloop()
