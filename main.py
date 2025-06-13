#!/usr/bin/env python3
"""
Who's Your Pokémon! - A Python-based "Guess Who" inspired game
A two-player game where players try to guess each other's chosen Pokémon.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import json
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os


class AutocompleteEntry(tk.Frame):
    """
    Autocomplete text entry widget with fuzzy search functionality
    """
    def __init__(self, parent, values, **kwargs):
        super().__init__(parent)
        
        self.values = values
        self.var = tk.StringVar()
        self.var.trace('w', self.on_text_changed)
        
        # Entry widget with better visual feedback
        self.entry = tk.Entry(
            self,
            textvariable=self.var,
            font=('Arial', 14),
            bg='#cccccc',
            fg='#222222',
            insertbackground='blue',  # Cursor color - more visible
            insertwidth=3,  # Wider cursor
            relief='solid',
            borderwidth=2,
            highlightbackground='#003a70',
            highlightcolor='#003a70',
            highlightthickness=2,
            **kwargs
        )
        self.entry.pack(fill='x')
        
        # Listbox for suggestions (initially hidden)
        self.listbox = tk.Listbox(
            self,
            height=8,
            font=('Arial', 12),
            bg='#cccccc',
            fg='#222222',
            selectbackground='#3d7dca',
            selectforeground='white',
            relief='solid',
            borderwidth=1
        )
        
        # Bind events
        self.entry.bind('<Down>', self.on_down_arrow)
        self.entry.bind('<Up>', self.on_up_arrow)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Tab>', self.on_tab)
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<KeyPress>', self.on_key_press)  # Track typing
        
        self.listbox.bind('<Button-1>', self.on_select)
        self.listbox.bind('<ButtonRelease-1>', self.on_select)  # Also handle release
        self.listbox.bind('<Double-Button-1>', self.on_double_click)
        self.listbox.bind('<Return>', self.on_enter)
        self.listbox.bind('<FocusOut>', self.on_listbox_focus_out)
        
        self.suggestions_visible = False
        self.selecting_from_list = False
        self.selection_made = False  # Track if user made a selection
    
    def fuzzy_search(self, query, items):
        """
        Perform fuzzy search on items based on query
        Returns list of items that match the query
        """
        if not query:
            return []
        
        query = query.lower()
        matches = []
        
        for item in items:
            item_lower = item.lower()
            
            # Exact match gets highest priority
            if item_lower == query:
                matches.insert(0, item)
            # Starts with query gets second priority
            elif item_lower.startswith(query):
                matches.append(item)
            # Contains query gets third priority
            elif query in item_lower:
                matches.append(item)
            # Fuzzy match - all characters of query appear in order
            else:
                query_index = 0
                for char in item_lower:
                    if query_index < len(query) and char == query[query_index]:
                        query_index += 1
                
                if query_index == len(query):
                    matches.append(item)
        
        return matches[:20]  # Limit to 20 suggestions
    
    def on_text_changed(self, *args):
        """Handle text changes in the entry widget"""
        if self.selecting_from_list:
            return
        
        # Don't show suggestions if user made a selection and hasn't typed since
        if self.selection_made:
            return
            
        query = self.var.get()
        matches = self.fuzzy_search(query, self.values)
        
        if matches and len(query) > 0:
            self.show_suggestions(matches)
        else:
            self.hide_suggestions()
    
    def on_key_press(self, event):
        """Handle key press events to detect typing"""
        # User is typing, reset selection flag
        self.selection_made = False
    
    def show_suggestions(self, matches):
        """Show the suggestions listbox with matching items"""
        self.listbox.delete(0, tk.END)
        for match in matches:
            self.listbox.insert(tk.END, match)
        
        if not self.suggestions_visible:
            self.listbox.pack(fill='x', pady=(2, 0))
            self.suggestions_visible = True
    
    def hide_suggestions(self):
        """Hide the suggestions listbox"""
        if self.suggestions_visible:
            self.listbox.pack_forget()
            self.suggestions_visible = False
    
    def on_focus_in(self, event):
        """Handle entry gaining focus"""
        self.entry.configure(relief='solid', borderwidth=3, highlightbackground='#003a70', bg='#cccccc')
        # Show suggestions if there's text
        if self.var.get():
            self.on_text_changed()
    
    def on_focus_out(self, event):
        """Handle entry losing focus"""
        self.entry.configure(relief='solid', borderwidth=1, highlightbackground='#003a70', bg='#cccccc')
        # Delay hiding to allow for mouse clicks on listbox
        self.after(200, self.check_and_hide_suggestions)
    
    def on_listbox_focus_out(self, event):
        """Handle listbox losing focus"""
        self.after(200, self.check_and_hide_suggestions)
    
    def check_and_hide_suggestions(self):
        """Check if focus is still in widget before hiding"""
        try:
            focused = self.focus_get()
            if focused != self.entry and focused != self.listbox:
                self.hide_suggestions()
        except:
            self.hide_suggestions()
    
    def on_down_arrow(self, event):
        """Handle down arrow key - move to listbox"""
        if self.suggestions_visible and self.listbox.size() > 0:
            self.listbox.focus_set()
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return 'break'
    
    def on_up_arrow(self, event):
        """Handle up arrow key"""
        if self.suggestions_visible and self.listbox.size() > 0:
            self.listbox.focus_set()
            last_index = self.listbox.size() - 1
            self.listbox.selection_set(last_index)
            self.listbox.activate(last_index)
            return 'break'
    
    def on_enter(self, event):
        """Handle enter key - select current item"""
        if self.suggestions_visible:
            selection = self.listbox.curselection()
            if selection:
                self.select_item(selection[0])
                return 'break'
            elif self.listbox.size() > 0:
                # Select first item if nothing is selected
                self.select_item(0)
                return 'break'
    
    def on_tab(self, event):
        """Handle tab key - select first suggestion"""
        if self.suggestions_visible and self.listbox.size() > 0:
            self.select_item(0)
            return 'break'
    
    def on_select(self, event):
        """Handle mouse selection from listbox"""
        selection = self.listbox.curselection()
        if selection:
            self.select_item(selection[0])
            return 'break'
    
    def on_double_click(self, event):
        """Handle double-click selection from listbox"""
        selection = self.listbox.curselection()
        if selection:
            self.select_item(selection[0])
            return 'break'
    
    def select_item(self, index):
        """Select an item from the listbox"""
        if 0 <= index < self.listbox.size():
            selected_item = self.listbox.get(index)
            self.selecting_from_list = True
            self.var.set(selected_item)
            self.selecting_from_list = False
            self.selection_made = True  # Mark that selection was made
            self.hide_suggestions()
            self.entry.focus_set()
            # Move cursor to end
            self.entry.icursor(tk.END)
    
    def get(self):
        """Get the current value"""
        return self.var.get()
    
    def set(self, value):
        """Set the current value"""
        self.var.set(value)


class PokemonGuessGame:
    def __init__(self):
        # Load Pokémon data from JSON file
        self.pokemon_data = self.load_pokemon_data()
        self.pokemon_list = list(self.pokemon_data.keys()) if self.pokemon_data else [
            "Pikachu", "Bulbasaur", "Charmander", "Squirtle", "Caterpie", "Weedle",
            "Pidgey", "Rattata", "Spearow", "Ekans", "Sandshrew", "Nidoran♀",
            "Nidoran♂", "Clefairy", "Vulpix", "Jigglypuff", "Zubat", "Oddish",
            "Paras", "Venonat", "Diglett", "Meowth", "Psyduck", "Mankey"
        ]
        
        # Image cache for sprites
        self.image_cache = {}
        self.x_icon = None  # Will store the X icon image
        self.image_size = (70, 70)  # Size for grid images
        
        # Game state
        self.player1_name = ""
        self.player2_name = ""
        self.player1_chosen = ""
        self.player2_chosen = ""
        self.current_player = 1
        self.game_active = False
        
        # Grid data
        self.player1_grid = []
        self.player2_grid = []
        self.player1_buttons = []
        self.player2_buttons = []
        self.player1_eliminated = set()
        self.player2_eliminated = set()
        
        # UI components
        self.root = None
        self.main_frame = None
        self.player1_name_label = None
        self.player2_name_label = None
        self.player1_remaining_label = None
        self.player2_remaining_label = None
        
        self.init_ui()
    
    def load_pokemon_data(self):
        """Load Pokémon data from the JSON file"""
        try:
            with open('pokemon_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Loaded {len(data)} Pokémon from data file")
            return data
        except FileNotFoundError:
            print("⚠️  Pokémon data file not found, using fallback list")
            return None
        except Exception as e:
            print(f"❌ Error loading Pokémon data: {e}")
            return None
    
    def download_and_cache_image(self, pokemon_name):
        """Download and cache a Pokémon sprite image"""
        if pokemon_name in self.image_cache:
            return self.image_cache[pokemon_name]
        
        try:
            if pokemon_name not in self.pokemon_data:
                return None
            
            sprite_url = self.pokemon_data[pokemon_name]
            response = requests.get(sprite_url, timeout=10)
            response.raise_for_status()
            
            # Open image and resize with proper margin
            image = Image.open(BytesIO(response.content))
            
            # Calculate size with 5px margin (75x75 for 80px button)
            target_size = 70  # 80 - 10 for margins
            image = image.resize((target_size, target_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(image)
            
            # Cache the image
            self.image_cache[pokemon_name] = photo
            return photo
            
        except Exception as e:
            print(f"❌ Error loading image for {pokemon_name}: {e}")
            return None
    
    def load_x_icon(self):
        """Load and prepare the X icon for elimination overlay"""
        try:
            x_image = Image.open('x_icon.png')
            x_image = x_image.resize((70, 70), Image.Resampling.LANCZOS)
            self.x_icon = ImageTk.PhotoImage(x_image)
            print("✅ X icon loaded successfully")
        except Exception as e:
            print(f"❌ Error loading X icon: {e}")
            self.x_icon = None
    
    def init_ui(self):
        """Initialize the main UI window"""
        self.root = tk.Tk()
        self.root.title("Who's Your Pokémon!")
        
        # Start with a regular sized window for debugging
        self.root.geometry("1000x700")
        self.root.configure(bg='#3d7dca')
        
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Allow escape key to close the window
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Load X icon after root window is created
        self.load_x_icon()
        
        self.show_startup_screen()
    
    def show_startup_screen(self):
        """Display the initial startup screen"""
        self.clear_screen()
        
        # Main container
        container = tk.Frame(self.root, bg='#3d7dca')
        container.pack(expand=True, fill='both')
        
        # Title
        title_label = tk.Label(
            container,
            text="Who's Your Pokémon!",
            font=('Arial', 48, 'bold'),
            fg='#003a70',
            bg='#3d7dca'
        )
        title_label.pack(pady=(100, 50))
        
        # Start button with rounded corners
        start_button = tk.Button(
            container,
            text="Start",
            font=('Arial', 24, 'bold'),
            bg='#ffcb05',
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            padx=50,
            pady=20,
            command=self.start_game,
            cursor='hand2'
        )
        start_button.pack(pady=20)
    
    def start_game(self):
        """Begin the game setup process"""
        self.setup_player(1)
    
    def setup_player(self, player_num):
        """Setup screen for player selection"""
        self.clear_screen()
        
        # Main container
        container = tk.Frame(self.root, bg='#3d7dca')
        container.pack(expand=True, fill='both')
        
        # Title
        title_label = tk.Label(
            container,
            text=f"Player {player_num} Setup",
            font=('Arial', 36, 'bold'),
            fg='#003a70',
            bg='#3d7dca'
        )
        title_label.pack(pady=(50, 30))
        
        # Name input
        name_label = tk.Label(
            container,
            text="Enter your name:",
            font=('Arial', 18),
            fg='#222222',
            bg='#3d7dca'
        )
        name_label.pack(pady=10)
        
        name_entry = tk.Entry(
            container,
            font=('Arial', 16),
            width=20,
            justify='center',
            bg='#cccccc',
            fg='#222222',
            relief='solid',
            borderwidth=2,
            highlightbackground='#003a70',
            highlightcolor='#003a70',
            highlightthickness=2
        )
        name_entry.pack(pady=10)
        name_entry.focus()
        
        # Pokemon selection
        pokemon_label = tk.Label(
            container,
            text="Choose your Pokémon (start typing to search):",
            font=('Arial', 18),
            fg='#222222',
            bg='#3d7dca'
        )
        pokemon_label.pack(pady=(30, 10))
        
        # Autocomplete entry for Pokemon selection
        pokemon_autocomplete = AutocompleteEntry(
            container,
            values=self.pokemon_list,
            width=25
        )
        pokemon_autocomplete.pack(pady=10)
        
        # Submit button
        def submit_player():
            name = name_entry.get().strip()
            chosen_pokemon = pokemon_autocomplete.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter your name!")
                return
            
            if not chosen_pokemon:
                messagebox.showerror("Error", "Please choose a Pokémon!")
                return
            
            # Validate that the chosen Pokemon exists in our list
            if chosen_pokemon not in self.pokemon_list:
                messagebox.showerror("Error", f"'{chosen_pokemon}' is not a valid Pokémon. Please select from the suggestions.")
                return
            
            if player_num == 1:
                self.player1_name = name
                self.player1_chosen = chosen_pokemon
                self.setup_player(2)
            else:
                self.player2_name = name
                self.player2_chosen = chosen_pokemon
                self.create_game_screen()
        
        submit_button = tk.Button(
            container,
            text="I Choose You!",
            font=('Arial', 18, 'bold'),
            bg='#ffcb05',
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            padx=30,
            pady=15,
            command=submit_player,
            cursor='hand2'
        )
        submit_button.pack(pady=30)
        
        # Bind Enter key to submit
        self.root.bind('<Return>', lambda e: submit_player())
    
    def create_game_screen(self):
        """Create the main game interface"""
        self.clear_screen()
        self.game_active = True
        
        # Generate grids
        self.generate_grids()
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#3d7dca')
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Title with increased font size (18 -> 22.5, rounded to 22)
        title_label = tk.Label(
            self.main_frame,
            text="Who's Your Pokémon!",
            font=('Arial', 22, 'bold'),
            fg='#003a70',
            bg='#3d7dca'
        )
        title_label.pack(pady=(0, 10))
        
        # Create horizontal layout using pack with equal distribution
        game_frame = tk.Frame(self.main_frame, bg='#3d7dca')
        game_frame.pack(expand=True, fill='both')
        
        # Player 1 side (LEFT) - force exactly half width
        player1_frame = tk.Frame(game_frame, bg='#3d7dca', width=400)
        player1_frame.pack(side='left', expand=True, fill='both', padx=(0, 2))
        player1_frame.pack_propagate(False)  # Maintain width
        
        # Remove "(Player 1)" suffix and increase font size by 25% (14 -> 17.5, rounded to 18)
        self.player1_name_label = tk.Label(
            player1_frame,
            text=f"{self.player1_name}",
            font=('Arial', 18, 'bold'),
            bg='lightgreen',
            relief='solid',
            borderwidth=2,
            padx=10,
            pady=15
        )
        self.player1_name_label.pack(pady=(0, 5))
        
        self.player1_remaining_label = tk.Label(
            player1_frame,
            text="Remaining: 24",
            font=('Arial', 11),
            bg='#3d7dca'
        )
        self.player1_remaining_label.pack(pady=(0, 5))
        
        # Player 1 grid container - remove red border
        p1_grid_container = tk.Frame(player1_frame, bg='#3d7dca', relief='solid', borderwidth=1)
        p1_grid_container.pack(expand=True, fill='both', pady=(0, 10))
        
        p1_grid_frame = tk.Frame(p1_grid_container, bg='#3d7dca')
        p1_grid_frame.pack(expand=True, fill='both', padx=3, pady=3)
        
        print("About to create Player 1 grid...")
        self.create_grid(p1_grid_frame, 1)
        
        # Player 2 side (RIGHT) - force exactly half width
        player2_frame = tk.Frame(game_frame, bg='#3d7dca', width=400)
        player2_frame.pack(side='left', expand=True, fill='both', padx=(2, 0))
        player2_frame.pack_propagate(False)  # Maintain width
        
        # Remove "(Player 2)" suffix and increase font size by 25%
        self.player2_name_label = tk.Label(
            player2_frame,
            text=f"{self.player2_name}",
            font=('Arial', 18, 'bold'),
            bg='lightcoral',
            relief='solid',
            borderwidth=2,
            padx=10,
            pady=15
        )
        self.player2_name_label.pack(pady=(0, 5))
        
        self.player2_remaining_label = tk.Label(
            player2_frame,
            text="Remaining: 24",
            font=('Arial', 11),
            bg='#3d7dca'
        )
        self.player2_remaining_label.pack(pady=(0, 5))
        
        # Player 2 grid container - remove red border
        p2_grid_container = tk.Frame(player2_frame, bg='#3d7dca', relief='solid', borderwidth=1)
        p2_grid_container.pack(expand=True, fill='both', pady=(0, 10))
        
        p2_grid_frame = tk.Frame(p2_grid_container, bg='#3d7dca')
        p2_grid_frame.pack(expand=True, fill='both', padx=3, pady=3)
        
        print("About to create Player 2 grid...")
        self.create_grid(p2_grid_frame, 2)
        
        # Control buttons at the bottom
        control_frame = tk.Frame(self.main_frame, bg='#3d7dca')
        control_frame.pack(pady=10)
        
        self.end_turn_button = tk.Button(
            control_frame,
            text="End Turn",
            font=('Arial', 12, 'bold'),
            bg='#ffcb05',
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            padx=20,
            pady=5,
            command=self.end_turn
        )
        self.end_turn_button.pack(side='left', padx=10)
        
        self.guess_button = tk.Button(
            control_frame,
            text="Make Guess",
            font=('Arial', 12, 'bold'),
            bg='#ffcb05',
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            padx=20,
            pady=5,
            command=self.make_guess
        )
        self.guess_button.pack(side='left', padx=10)
        
        print("Game screen layout complete. Updating turn indicator...")
        self.update_turn_indicator()
        
        # Force layout refresh
        self.root.update_idletasks()
        print("Game screen creation finished!")
    
    def generate_grids(self):
        """Generate the Pokemon grids for both players"""
        print(f"Generating grids. Player 1 chose: {self.player1_chosen}, Player 2 chose: {self.player2_chosen}")
        
        # Create Player 1's grid - select 24 random Pokémon from the full list
        available_pokemon = self.pokemon_list.copy()
        
        # Ensure Player 1's chosen Pokemon is included
        if self.player1_chosen in available_pokemon:
            available_pokemon.remove(self.player1_chosen)
        
        # Select 23 random Pokemon and add the chosen one
        self.player1_grid = random.sample(available_pokemon, 23)
        self.player1_grid.append(self.player1_chosen)
        random.shuffle(self.player1_grid)
        
        # Create Player 2's grid - select 24 random Pokémon from the full list
        available_pokemon = self.pokemon_list.copy()
        
        # Ensure Player 2's chosen Pokemon is included
        if self.player2_chosen in available_pokemon:
            available_pokemon.remove(self.player2_chosen)
        
        # Select 23 random Pokemon and add the chosen one
        self.player2_grid = random.sample(available_pokemon, 23)
        self.player2_grid.append(self.player2_chosen)
        random.shuffle(self.player2_grid)
        
        print(f"Player 1 grid: {self.player1_grid[:6]}...")  # Show first 6
        print(f"Player 2 grid: {self.player2_grid[:6]}...")  # Show first 6
    
    def create_grid(self, parent, player):
        """Create a 6x4 grid of Pokemon buttons with uniform sizing"""
        grid_data = self.player1_grid if player == 1 else self.player2_grid
        button_list = []
        
        # Debug print to ensure this method is called
        print(f"Creating grid for player {player} with {len(grid_data)} Pokemon")
        
        # Fixed button size for uniform grid
        button_size = 80
        
        for row in range(4):
            button_row = []
            for col in range(6):
                idx = row * 6 + col
                if idx < len(grid_data):
                    pokemon_name = grid_data[idx]
                    
                    # Try to get the sprite image
                    sprite_image = self.download_and_cache_image(pokemon_name)
                    
                    button = tk.Button(
                        parent,
                        bg='#FFFFFF',
                        fg='#333333',
                        relief='raised',
                        borderwidth=1,
                        compound='center',
                        command=lambda p=pokemon_name, pl=player: self.toggle_pokemon(p, pl)
                    )
                    
                    # Set image if available, otherwise use text with wrapping
                    if sprite_image:
                        button.configure(
                            image=sprite_image,
                            text="",
                            compound='center',
                            width=button_size,
                            height=button_size
                        )
                        # Keep a reference to prevent garbage collection
                        button.image = sprite_image
                    else:
                        button.configure(
                            text=pokemon_name,
                            font=('Arial', 7, 'bold'),
                            wraplength=button_size - 10,
                            justify='center',
                            compound='center',
                            width=button_size,
                            height=button_size
                        )
                    
                    button.grid(row=row, column=col, padx=2, pady=2, sticky='')
                    button_row.append(button)
                    print(f"Created button for {pokemon_name} at ({row}, {col})")
            
            if button_row:  # Only add non-empty rows
                button_list.append(button_row)
        
        # Configure grid weights for uniform distribution with minimum sizes
        for i in range(4):
            parent.grid_rowconfigure(i, weight=1, minsize=button_size + 4, uniform="row")
        for i in range(6):
            parent.grid_columnconfigure(i, weight=1, minsize=button_size + 4, uniform="col")
        
        # Store the button references
        if player == 1:
            self.player1_buttons = button_list
            print(f"Player 1 buttons stored: {len(button_list)} rows")
        else:
            self.player2_buttons = button_list
            print(f"Player 2 buttons stored: {len(button_list)} rows")
        
        # Force update to ensure widgets are displayed
        parent.update_idletasks()
    
    def toggle_pokemon(self, pokemon, player_grid):
        """Toggle elimination of a Pokemon"""
        if not self.game_active:
            return
        
        # Players can only click on opponent's grid
        if (self.current_player == 1 and player_grid == 1) or \
           (self.current_player == 2 and player_grid == 2):
            return
        
        # Find the button
        button = None
        grid_data = self.player1_grid if player_grid == 1 else self.player2_grid
        buttons = self.player1_buttons if player_grid == 1 else self.player2_buttons
        eliminated_set = self.player1_eliminated if player_grid == 1 else self.player2_eliminated
        
        # Find button position
        try:
            idx = grid_data.index(pokemon)
            row = idx // 6
            col = idx % 6
            button = buttons[row][col]
        except (ValueError, IndexError):
            return
        
        # Toggle elimination
        if pokemon in eliminated_set:
            # Remove elimination - restore original image/text
            eliminated_set.remove(pokemon)
            sprite_image = self.download_and_cache_image(pokemon)
            
            # Restore original content while maintaining button size
            button.configure(
                bg='#FFFFFF',
                fg='#333333',
                relief='raised'
            )
            
            if sprite_image:
                button.configure(
                    image=sprite_image,
                    text="",
                    compound='center',
                    width=80,
                    height=80
                )
                button.image = sprite_image
            else:
                button.configure(
                    text=pokemon,
                    image="",
                    font=('Arial', 7, 'bold'),
                    wraplength=70,
                    justify='center',
                    compound='center',
                    width=80,
                    height=80
                )
        else:
            # Add elimination - show X icon or red X text
            eliminated_set.add(pokemon)
            button.configure(
                bg='#F44336',
                fg='white',
                relief='sunken'
            )
            
            if self.x_icon:
                # Use X icon overlay - ensure button size stays the same
                button.configure(
                    image=self.x_icon,
                    text="",
                    compound='center',
                    width=80,
                    height=80
                )
                button.image = self.x_icon
            else:
                # Fallback to text X with same sizing
                button.configure(
                    text='X',
                    image="",
                    font=('Arial', 20, 'bold'),
                    compound='center',
                    width=80,
                    height=80
                )
        
        self.update_remaining_count()
    
    def update_remaining_count(self):
        """Update the remaining Pokemon count"""
        remaining1 = 24 - len(self.player1_eliminated)
        remaining2 = 24 - len(self.player2_eliminated)
        
        self.player1_remaining_label.configure(text=f"Remaining: {remaining1}")
        self.player2_remaining_label.configure(text=f"Remaining: {remaining2}")
    
    def update_turn_indicator(self):
        """Update visual indication of current player"""
        if self.current_player == 1:
            self.player1_name_label.configure(bg='#4CAF50', fg='white')
            self.player2_name_label.configure(bg='#E3F2FD', fg='#333')
        else:
            self.player1_name_label.configure(bg='#E3F2FD', fg='#333')
            self.player2_name_label.configure(bg='#4CAF50', fg='white')
    
    def end_turn(self):
        """End current player's turn"""
        if not self.game_active:
            return
        
        # Check if current player eliminated opponent's chosen Pokemon
        opponent_chosen = self.player2_chosen if self.current_player == 1 else self.player1_chosen
        opponent_eliminated = self.player2_eliminated if self.current_player == 1 else self.player1_eliminated
        
        if opponent_chosen in opponent_eliminated:
            # Current player loses
            current_player_name = self.player1_name if self.current_player == 1 else self.player2_name
            self.end_game(f"{current_player_name} Loses!", f"{current_player_name} accidentally eliminated their target!")
            return
        
        # Switch turns
        self.current_player = 2 if self.current_player == 1 else 1
        self.update_turn_indicator()
    
    def make_guess(self):
        """Allow current player to make a guess"""
        if not self.game_active:
            return
        
        current_player_name = self.player1_name if self.current_player == 1 else self.player2_name
        opponent_chosen = self.player2_chosen if self.current_player == 1 else self.player1_chosen
        
        # Get non-eliminated Pokemon from opponent's grid
        opponent_grid = self.player2_grid if self.current_player == 1 else self.player1_grid
        opponent_eliminated = self.player2_eliminated if self.current_player == 1 else self.player1_eliminated
        available_pokemon = [pokemon for pokemon in opponent_grid if pokemon not in opponent_eliminated]
        
        # Create guess dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Make a Guess")
        dialog.geometry("350x250")
        dialog.configure(bg='#3d7dca')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Guess your opponent's Pokémon:",
            font=('Arial', 14),
            fg='#222222',
            bg='#3d7dca'
        ).pack(pady=20)
        
        # Regular dropdown with only available Pokemon
        guess_var = tk.StringVar()
        guess_dropdown = ttk.Combobox(
            dialog,
            textvariable=guess_var,
            values=sorted(available_pokemon),
            state="readonly",
            font=('Arial', 12),
            width=25
        )
        
        # Style the combobox to match our color scheme
        style = ttk.Style()
        style.configure('Custom.TCombobox',
                       fieldbackground='#cccccc',
                       background='#cccccc',
                       foreground='#222222',
                       borderwidth=2,
                       relief='solid')
        
        guess_dropdown.configure(style='Custom.TCombobox')
        guess_dropdown.pack(pady=10)
        
        def submit_guess():
            guess = guess_var.get().strip()
            if not guess:
                messagebox.showerror("Error", "Please select a Pokémon!")
                return
            
            dialog.destroy()
            
            if guess == opponent_chosen:
                self.end_game(f"{current_player_name} Wins!", f"{current_player_name} correctly guessed {opponent_chosen}!")
            else:
                self.end_game(f"{current_player_name} Loses!", f"{current_player_name} guessed {guess}, but it was {opponent_chosen}!")
        
        tk.Button(
            dialog,
            text="Submit Guess",
            font=('Arial', 12, 'bold'),
            bg='#ffcb05',
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            command=submit_guess,
            cursor='hand2'
        ).pack(pady=20)
    
    def end_game(self, result, message):
        """End the game and show results"""
        self.game_active = False
        self.clear_screen()
        
        # Main container
        container = tk.Frame(self.root, bg='#3d7dca')
        container.pack(expand=True, fill='both')
        
        # Result
        result_label = tk.Label(
            container,
            text=result,
            font=('Arial', 48, 'bold'),
            fg='#4CAF50' if 'Wins' in result else '#F44336',
            bg='#3d7dca'
        )
        result_label.pack(pady=(100, 20))
        
        # Message
        message_label = tk.Label(
            container,
            text=message,
            font=('Arial', 18),
            fg='#222222',
            bg='#3d7dca'
        )
        message_label.pack(pady=20)
        
        # New game button
        new_game_button = tk.Button(
            container,
            text="New Game",
            font=('Arial', 20, 'bold'),
            bg='#ffcb05',
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            padx=40,
            pady=15,
            command=self.new_game,
            cursor='hand2'
        )
        new_game_button.pack(pady=40)
    
    def new_game(self):
        """Start a new game"""
        # Reset game state
        self.player1_name = ""
        self.player2_name = ""
        self.player1_chosen = ""
        self.player2_chosen = ""
        self.current_player = 1
        self.game_active = False
        self.player1_grid = []
        self.player2_grid = []
        self.player1_buttons = []
        self.player2_buttons = []
        self.player1_eliminated = set()
        self.player2_eliminated = set()
        
        # Show startup screen
        self.show_startup_screen()
    
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Unbind Enter key
        self.root.unbind('<Return>')
    
    def run(self):
        """Start the game"""
        self.root.mainloop()


def main():
    """Main function to run the game"""
    game = PokemonGuessGame()
    game.run()


if __name__ == "__main__":
    main()
