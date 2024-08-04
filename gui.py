import pandas as pd
import tkinter as tk
from tkinter import ttk

# Load the data
qb_results = pd.read_csv('final_data/qb_final_predictions.csv')
rb_results = pd.read_csv('final_data/rb_final_predictions.csv')
wr_results = pd.read_csv('final_data/wr_final_predictions.csv')
te_results = pd.read_csv('final_data/te_final_predictions.csv')

# Create the main application window
root = tk.Tk()
root.title('Fantasy Football Predictions')

# Create a notebook widget to hold the tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create frames for each position
frames = {
    'Quarterbacks': qb_results,
    'Running Backs': rb_results,
    'Wide Receivers': wr_results,
    'Tight Ends': te_results,
    'All Players': pd.concat([qb_results, rb_results, wr_results, te_results]).sort_values(by='fantasy_points', ascending=False),
    'Drafted Players': pd.DataFrame(columns=qb_results.columns)  # Initially empty
}

# List to keep track of struck-through players
struck_players = set()

# Function to toggle strikethrough
def toggle_strikethrough(event):
    item = event.widget.selection()[0]
    player_name = event.widget.item(item, 'text')
    
    # Do not allow strikethrough for players in "Drafted Players"
    if player_name in frames['Drafted Players']['display_name'].values:
        return
    
    if player_name in struck_players:
        struck_players.remove(player_name)
    else:
        struck_players.add(player_name)
    
    # Refresh all frames to update styles
    for tab_name, data in frames.items():
        display_predictions(frame_widgets[tab_name], data, search_entry.get())

# Function to display predictions in a treeview
def display_predictions(frame, results, search_query=''):
    # Clear existing treeview if any
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Filter results based on search query
    if search_query:
        results = results[results['display_name'].str.contains(search_query, case=False, na=False)]
    
    tree = ttk.Treeview(frame, columns=list(results.columns), show='headings')
    tree.pack(expand=True, fill='both')
    
    # Define columns
    for col in results.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    # Insert data with strikethrough or green font where applicable
    for _, row in results.iterrows():
        player_name = row['display_name']
        if player_name in frames['Drafted Players']['display_name'].values:
            tags = ('drafted',)
        elif player_name in struck_players:
            tags = ('struck',)
        else:
            tags = ('',)
        tree.insert('', 'end', text=player_name, values=list(row), tags=tags)
    
    # Add tag configuration for strikethrough and drafted
    tree.tag_configure('struck', font=('Helvetica', 10, 'overstrike'))
    tree.tag_configure('drafted', foreground='green')
    
    # Bind the click event to toggle strikethrough
    tree.bind('<Double-1>', toggle_strikethrough)
    tree.bind('<Button-3>', lambda event: show_context_menu(event, tree, results))

# Function to handle search
def search_predictions():
    search_query = search_entry.get()
    for tab_name, data in frames.items():
        display_predictions(frame_widgets[tab_name], data, search_query)

# Function to add player to drafted list
def add_to_drafted(player_data):
    drafted_df = frames['Drafted Players']
    if player_data['display_name'] not in drafted_df['display_name'].values:
        frames['Drafted Players'] = pd.concat([drafted_df, player_data.to_frame().T], ignore_index=True)
    display_predictions(frame_widgets['Drafted Players'], frames['Drafted Players'], search_entry.get())

# Function to remove player from drafted list
def remove_from_drafted(player_name):
    frames['Drafted Players'] = frames['Drafted Players'][frames['Drafted Players']['display_name'] != player_name]
    display_predictions(frame_widgets['Drafted Players'], frames['Drafted Players'], search_entry.get())

# Function to show context menu
def show_context_menu(event, tree, results):
    item = tree.identify_row(event.y)
    if item:
        player_name = tree.item(item, 'text')
        player_data = results[results['display_name'] == player_name].iloc[0]

        context_menu = tk.Menu(root, tearoff=0)
        if player_name in frames['Drafted Players']['display_name'].values:
            context_menu.add_command(label="Remove from Drafted", command=lambda: remove_from_drafted(player_name))
        elif player_name not in struck_players:
            context_menu.add_command(label="Add to Drafted", command=lambda: add_to_drafted(player_data))
        context_menu.post(event.x_root, event.y_root)

# Create a search bar and button
search_frame = ttk.Frame(root)
search_frame.pack(fill='x')
search_label = ttk.Label(search_frame, text='Search Player:')
search_label.pack(side='left', padx=5, pady=5)
search_entry = ttk.Entry(search_frame)
search_entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)
search_button = ttk.Button(search_frame, text='Search', command=search_predictions)
search_button.pack(side='left', padx=5, pady=5)

# Add tabs and display data
frame_widgets = {}
for tab_name, data in frames.items():
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tab_name)
    frame_widgets[tab_name] = frame
    display_predictions(frame, data)

# Start the main event loop
root.mainloop()
