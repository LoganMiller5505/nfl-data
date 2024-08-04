import pandas as pd
import tkinter as tk
from tkinter import ttk

# Load the data
qb_results = pd.read_csv('final_data/qb_final_predictions.csv')
rb_results = pd.read_csv('final_data/rb_final_predictions.csv')
wr_results = pd.read_csv('final_data/wr_final_predictions.csv')
te_results = pd.read_csv('final_data/te_final_predictions.csv')

class FantasyFootballApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Fantasy Football Predictions')

        # Initialize variables
        self.drafted_players = {
            'QB': [],
            'RB': [],
            'WR': [],
            'TE': [],
            'FLEX': [],
            'BENCH': []
        }
        self.drafted_counts = {
            'QB': 0,
            'RB': 0,
            'WR': 0,
            'TE': 0,
            'FLEX': 0,
            'BENCH': 0
        }
        self.struck_players = set()

        # Create search bar
        self.create_search_bar()

        # Create the main layout
        self.create_tabs()

    def create_search_bar(self):
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill='x')
        search_label = ttk.Label(search_frame, text='Search Player:')
        search_label.pack(side='left', padx=5, pady=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
        search_button = ttk.Button(search_frame, text='Search', command=self.refresh_all_frames)
        search_button.pack(side='left', padx=5, pady=5)

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
            'Drafted Players': pd.DataFrame(columns=['display_name', 'fantasy_points', 'position'])  # Initially empty
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
            tree = ttk.Treeview(position_frame, columns=('display_name', 'fantasy_points'), show='headings', height=5)
            tree.pack(expand=True, fill='both')
            self.position_frames[position] = tree

    def refresh_all_frames(self):
        for tab_name, data in self.frames.items():
            if tab_name == 'Drafted Players':
                self.refresh_drafted_section()
            else:
                self.display_predictions(self.frame_widgets[tab_name], data)

    def display_predictions(self, frame, results):
        # Clear existing treeview if any
        for widget in frame.winfo_children():
            widget.destroy()

        # Filter results based on search query
        search_query = self.search_entry.get()
        if search_query:
            results = results[results['display_name'].str.contains(search_query, case=False, na=False)]

        tree = ttk.Treeview(frame, columns=('display_name', 'fantasy_points'), show='headings')
        tree.pack(expand=True, fill='both')

        # Define columns
        tree.heading('display_name', text='Player')
        tree.heading('fantasy_points', text='Fantasy Points')

        # Insert data with strikethrough where applicable
        for _, row in results.iterrows():
            player_name = row['display_name']
            fantasy_points = row['fantasy_points']
            tags = []

            if player_name in self.struck_players:
                tags.append('struck')

            tree.insert('', 'end', text=player_name, values=(player_name, fantasy_points), tags=tags)

        # Add tag configuration for strikethrough
        tree.tag_configure('struck', font=('Helvetica', 10, 'overstrike'))

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
        else:
            self.struck_players.add(player_name)

        # Refresh all frames to update styles
        self.refresh_all_frames()

    def get_all_drafted_players(self):
        return [player['display_name'] for position in self.drafted_players.values() for player in position]

    def add_to_drafted(self, player_data):
        position = player_data['position']
        
        # Add player to drafted counts with limits
        if position == 'QB' and self.drafted_counts['QB'] < 1:
            self.drafted_counts['QB'] += 1
            self.drafted_players['QB'].append(player_data)
        elif position == 'RB' and self.drafted_counts['RB'] < 2:
            self.drafted_counts['RB'] += 1
            self.drafted_players['RB'].append(player_data)
        elif position == 'WR' and self.drafted_counts['WR'] < 2:
            self.drafted_counts['WR'] += 1
            self.drafted_players['WR'].append(player_data)
        elif position == 'TE' and self.drafted_counts['TE'] < 1:
            self.drafted_counts['TE'] += 1
            self.drafted_players['TE'].append(player_data)
        elif position in ['RB', 'WR', 'TE'] and self.drafted_counts['FLEX'] < 1:
            self.drafted_counts['FLEX'] += 1
            self.drafted_players['FLEX'].append(player_data)
        elif self.drafted_counts['BENCH'] < 7:
            self.drafted_counts['BENCH'] += 1
            self.drafted_players['BENCH'].append(player_data)
        else:
            return  # Limit reached; do not add player

        self.refresh_drafted_section()  # Refresh only the drafted section

    def remove_from_drafted(self, player_data):
        position = player_data['position']
        self.drafted_players[position].remove(player_data)

        # Decrement the appropriate count
        if position == 'QB':
            self.drafted_counts['QB'] -= 1
        elif position == 'RB':
            self.drafted_counts['RB'] -= 1
        elif position == 'WR':
            self.drafted_counts['WR'] -= 1
        elif position == 'TE':
            self.drafted_counts['TE'] -= 1
        elif position in ['RB', 'WR', 'TE']:
            self.drafted_counts['FLEX'] -= 1
        self.drafted_counts['BENCH'] -= 1

        self.refresh_drafted_section()  # Refresh only the drafted section

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
                    tree.insert('', 'end', text=player['display_name'], values=(player['display_name'], player['fantasy_points']))

# Start the main event loop
if __name__ == "__main__":
    root = tk.Tk()
    app = FantasyFootballApp(root)
    root.mainloop()
