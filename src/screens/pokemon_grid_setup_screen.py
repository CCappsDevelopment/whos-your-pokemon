"""
Pokemon Grid Setup screen for manual Pokemon selection
"""
import tkinter as tk
from tkinter import messagebox
from .base_screen import BaseScreen
from ..widgets import AutocompleteEntry
from ..utils import get_title_font, get_subtitle_font, get_grid_font, get_small_font, bind_mousewheel


class PokemonGridSetupScreen(BaseScreen):
    """Screen for manual Pokemon grid setup"""
    
    def __init__(self, root, game):
        super().__init__(root, game)
        self.current_player = None
        self.chosen_pokemon = None
        self.grid_tiles = []  # Will store the tile widgets
        self.autocomplete_widgets = []  # Will store autocomplete widgets
        self.selected_pokemon = {}  # Maps position (row, col) to pokemon name
        self.used_pokemon = set()  # Track which Pokemon have been used
        self.confirm_button = None
    
    def show(self, player_num, player_name, chosen_pokemon):
        """Show the manual grid setup screen"""
        self.clear_screen()
        
        self.current_player = player_num
        self.chosen_pokemon = chosen_pokemon
        
        # Initialize used Pokemon set with the chosen Pokemon
        self.used_pokemon = {chosen_pokemon}
        
        # Store player info for later use
        if player_num == 1:
            self.game.player1_name = player_name
            self.game.player1_chosen = chosen_pokemon
        else:
            self.game.player2_name = player_name
            self.game.player2_chosen = chosen_pokemon
        
        # Main container - centered and constrained
        self.container = tk.Frame(self.root, bg='#3d7dca')
        self.container.pack(expand=True, fill='both')
        
        # Create centered content frame with maximum dimensions
        self.content_frame = tk.Frame(self.container, bg='#3d7dca')
        self.content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        self._create_content(player_name)
        
    def _create_content(self, player_name):
        """Create the main content of the screen"""
        # Logo
        logo_image = self.game.image_loader.load_logo_image('pokemon-grid-setup-logo.png', max_width=500, max_height=80)
        if logo_image:
            logo_label = tk.Label(
                self.content_frame,
                image=logo_image,
                bg='#3d7dca'
            )
            logo_label.image = logo_image  # Keep reference
            logo_label.pack(pady=(10, 15))
        else:
            # Fallback text
            title_label = tk.Label(
                self.content_frame,
                text="Pokemon Grid Setup",
                font=get_title_font(),
                fg='#003a70',
                bg='#3d7dca'
            )
            title_label.pack(pady=(10, 15))
        
        # Player instruction
        instruction_label = tk.Label(
            self.content_frame,
            text=f"{player_name}, choose the Pokemon for your grid.",
            font=get_subtitle_font(),
            fg='#003a70',
            bg='#3d7dca'
        )
        instruction_label.pack(pady=(0, 20))
        
        # Create the grid
        self._create_pokemon_grid()
        
        # Confirm button with matching app styling
        self.confirm_button = tk.Button(
            self.content_frame,
            text="Confirm Grid",
            font=get_subtitle_font(),
            bg='#cccccc',  # Disabled color initially
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            padx=30,
            pady=10,
            state='disabled',
            cursor='hand2',
            command=self._confirm_selection
        )
        self.confirm_button.pack(pady=(20, 10))
        
    def _create_pokemon_grid(self):
        """Create the 6x4 Pokemon grid with autocomplete widgets"""
        # Grid container with fixed size
        grid_container = tk.Frame(self.content_frame, bg='#3d7dca')
        grid_container.pack(pady=10)
        
        # Create 6x4 grid (6 columns, 4 rows = 24 total)
        self.grid_tiles = []
        self.autocomplete_widgets = []
        self.selected_pokemon = {}
        
        # Determine where to place the chosen Pokemon (random position for now, can be made configurable)
        import random
        chosen_row, chosen_col = random.randint(0, 3), random.randint(0, 5)
        self.selected_pokemon[(chosen_row, chosen_col)] = self.chosen_pokemon
        
        for row in range(4):
            tile_row = []
            autocomplete_row = []
            
            for col in range(6):
                # Create container for each position with fixed size
                position_frame = tk.Frame(grid_container, bg='#3d7dca', width=80, height=120)
                position_frame.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
                position_frame.grid_propagate(False)  # Maintain fixed size
                
                # Create tile button with fixed size
                tile_button = tk.Button(
                    position_frame,
                    width=80,
                    height=80,
                    relief='solid',
                    borderwidth=2,
                    bg='#cccccc',
                    compound='center'
                )
                tile_button.pack(pady=(0, 5))
                
                # Check if this is the chosen Pokemon position
                if row == chosen_row and col == chosen_col:
                    # Load and display chosen Pokemon
                    self._load_pokemon_image_for_tile(tile_button, self.chosen_pokemon)
                    tile_button.configure(bg='#ffff00', borderwidth=4)  # Highlight chosen Pokemon
                    
                    # Add label for chosen Pokemon
                    chosen_label = tk.Label(
                        position_frame,
                        text="CHOSEN",
                        font=get_grid_font(),
                        fg='#003a70',
                        bg='#3d7dca'
                    )
                    chosen_label.pack()
                    
                    autocomplete_widget = None  # No autocomplete for chosen Pokemon
                else:
                    # Load pokeball image
                    self._load_pokeball_image_for_tile(tile_button)
                    
                    # Create autocomplete widget with fixed width and floating dropdown
                    autocomplete_widget = ConstrainedAutocompleteEntry(
                        position_frame,
                        values=self._get_available_pokemon(),
                        image_loader=self.game.image_loader,
                        data_manager=self.game.data_manager,
                        width=10,  # Fixed width
                        on_selection_callback=lambda pokemon, r=row, c=col: self._on_pokemon_selected(pokemon, r, c)
                    )
                    autocomplete_widget.pack()
                
                tile_row.append(tile_button)
                autocomplete_row.append(autocomplete_widget)
            
            self.grid_tiles.append(tile_row)
            self.autocomplete_widgets.append(autocomplete_row)
    
    def _get_available_pokemon(self):
        """Get list of Pokemon that haven't been used yet"""
        return [pokemon for pokemon in self.game.filtered_pokemon_list if pokemon not in self.used_pokemon]
    
    def _on_pokemon_selected(self, pokemon_name, row, col):
        """Handle Pokemon selection in grid"""
        if not pokemon_name or pokemon_name in self.used_pokemon:
            return
        
        # Remove previously selected Pokemon from this position if any
        old_pokemon = self.selected_pokemon.get((row, col))
        if old_pokemon and old_pokemon != self.chosen_pokemon:
            self.used_pokemon.discard(old_pokemon)
        
        # Add new Pokemon
        self.used_pokemon.add(pokemon_name)
        self.selected_pokemon[(row, col)] = pokemon_name
        
        # Update tile image
        tile_button = self.grid_tiles[row][col]
        self._load_pokemon_image_for_tile(tile_button, pokemon_name)
        tile_button.configure(bg='#cccccc', borderwidth=2)
        
        # Update all autocomplete widgets to remove this Pokemon from options
        self._update_all_autocompletes()
        
        # Update confirm button state
        self._update_confirm_button()
    
    def _update_all_autocompletes(self):
        """Update all autocomplete widgets with current available Pokemon"""
        available_pokemon = self._get_available_pokemon()
        
        for row in range(4):
            for col in range(6):
                autocomplete_widget = self.autocomplete_widgets[row][col]
                if autocomplete_widget:
                    autocomplete_widget.update_values(available_pokemon)
    
    def _load_pokemon_image_for_tile(self, tile_button, pokemon_name):
        """Load Pokemon image for a tile"""
        sprite_url = self.game.data_manager.get_pokemon_sprite_url(pokemon_name)
        if sprite_url:
            # Use autocomplete size since it's smaller and better for tiles
            image = self.game.image_loader.load_pokemon_image_autocomplete(pokemon_name, sprite_url)
            if image:
                tile_button.configure(image=image, text="")
                tile_button.image = image  # Keep reference
    
    def _load_pokeball_image_for_tile(self, tile_button):
        """Load pokeball image for a tile"""
        try:
            pokeball_image = self.game.image_loader.load_logo_image('pokeball.png', max_width=80, max_height=80)
            if pokeball_image:
                tile_button.configure(image=pokeball_image, text="")
                tile_button.image = pokeball_image  # Keep reference
        except Exception as e:
            print(f"⚠️ Could not load pokeball image: {e}")
            tile_button.configure(text="?", font=('Arial', 20), image="")
    
    def _update_confirm_button(self):
        """Update confirm button state based on grid completion"""
        # Check if all 24 positions are filled
        if len(self.selected_pokemon) == 24:
            self.confirm_button.configure(
                state='normal',
                bg='#ffcb05',  # Yellow like other app buttons
                fg='#222222'
            )
        else:
            self.confirm_button.configure(
                state='disabled',
                bg='#cccccc',  # Gray for disabled
                fg='#222222'
            )
    
    def _confirm_selection(self):
        """Confirm the manual Pokemon selection"""
        if len(self.selected_pokemon) != 24:
            messagebox.showwarning("Incomplete Grid", "Please fill all tiles before confirming.")
            return
        
        # Convert selected_pokemon dict to ordered list matching grid layout
        pokemon_grid = []
        for row in range(4):
            for col in range(6):
                pokemon_name = self.selected_pokemon.get((row, col))
                if pokemon_name:
                    pokemon_grid.append(pokemon_name)
                else:
                    messagebox.showerror("Error", f"Missing Pokemon at position ({row}, {col})")
                    return
        
        # Complete the grid setup through the game controller
        self.game.complete_player_grid_setup(self.current_player, pokemon_grid)


class ConstrainedAutocompleteEntry(tk.Frame):
    """
    Constrained autocomplete widget that doesn't resize and has floating dropdown
    """
    def __init__(self, parent, values, image_loader=None, data_manager=None, on_selection_callback=None, **kwargs):
        super().__init__(parent, bg='#3d7dca')
        
        self.values = values
        self.image_loader = image_loader
        self.data_manager = data_manager
        self.on_selection_callback = on_selection_callback
        self.var = tk.StringVar()
        self.var.trace('w', self.on_text_changed)
        
        # Entry widget with fixed width
        self.entry = tk.Entry(
            self,
            textvariable=self.var,
            font=get_small_font(),
            bg='#cccccc',
            fg='#222222',
            insertbackground='blue',
            insertwidth=2,
            relief='solid',
            borderwidth=1,
            highlightbackground='#003a70',
            highlightcolor='#003a70',
            highlightthickness=1,
            **kwargs
        )
        self.entry.pack()
        
        # Floating suggestions window (initially hidden)
        self.suggestions_window = None
        self.suggestion_items = []
        
        # Bind events
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<Button-1>', self.on_entry_click)
        
    def on_entry_click(self, event=None):
        """Show suggestions when entry is clicked"""
        self.show_suggestions()
        
    def on_text_changed(self, *args):
        """Handle text changes in entry"""
        self.show_suggestions()
        
    def show_suggestions(self):
        """Show floating suggestions window"""
        query = self.var.get().lower().strip()
        
        if not query:
            self.hide_suggestions()
            return
        
        # Filter values based on query
        matches = [value for value in self.values if query in value.lower()][:10]  # Limit to 10 matches
        
        if not matches:
            self.hide_suggestions()
            return
        
        # Create or update suggestions window
        if not self.suggestions_window:
            self.suggestions_window = tk.Toplevel(self)
            self.suggestions_window.wm_overrideredirect(True)
            self.suggestions_window.configure(bg='#cccccc', relief='solid', borderwidth=1)
        
        # Clear previous suggestions
        for item in self.suggestion_items:
            item.destroy()
        self.suggestion_items = []
        
        # Add new suggestions
        for match in matches:
            item_frame = tk.Frame(self.suggestions_window, bg='#cccccc')
            item_frame.pack(fill='x', padx=1, pady=1)
            
            # Pokemon name label
            name_label = tk.Label(
                item_frame,
                text=match,
                font=get_small_font(),
                bg='#cccccc',
                fg='#222222',
                anchor='w',
                padx=5,
                pady=2
            )
            name_label.pack(side='left', fill='x', expand=True)
            
            # Bind click events
            def make_select_func(pokemon_name):
                return lambda e: self.select_pokemon(pokemon_name)
            
            item_frame.bind('<Button-1>', make_select_func(match))
            name_label.bind('<Button-1>', make_select_func(match))
            
            # Hover effects
            def make_hover_funcs(frame, label):
                def on_enter(e):
                    frame.configure(bg='#0078d4')
                    label.configure(bg='#0078d4', fg='white')
                def on_leave(e):
                    frame.configure(bg='#cccccc')
                    label.configure(bg='#cccccc', fg='#222222')
                return on_enter, on_leave
            
            enter_func, leave_func = make_hover_funcs(item_frame, name_label)
            item_frame.bind('<Enter>', enter_func)
            item_frame.bind('<Leave>', leave_func)
            name_label.bind('<Enter>', enter_func)
            name_label.bind('<Leave>', leave_func)
            
            self.suggestion_items.append(item_frame)
        
        # Position the suggestions window
        self.position_suggestions_window()
        
    def position_suggestions_window(self):
        """Position the suggestions window relative to the entry"""
        if not self.suggestions_window:
            return
        
        # Get entry position
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        
        # Set window position and size
        self.suggestions_window.geometry(f"200x{min(len(self.suggestion_items) * 25, 250)}+{x}+{y}")
        
    def hide_suggestions(self):
        """Hide suggestions window"""
        if self.suggestions_window:
            self.suggestions_window.destroy()
            self.suggestions_window = None
            self.suggestion_items = []
            
    def on_focus_out(self, event=None):
        """Hide suggestions when focus is lost"""
        # Delay hiding to allow for clicks on suggestions
        self.after(150, self.hide_suggestions)
        
    def select_pokemon(self, pokemon_name):
        """Select a Pokemon from suggestions"""
        self.var.set(pokemon_name)
        self.hide_suggestions()
        if self.on_selection_callback:
            self.on_selection_callback(pokemon_name)
            
    def update_values(self, new_values):
        """Update available values"""
        self.values = new_values
        # If current entry value is no longer available, clear it
        current = self.var.get()
        if current and current not in new_values:
            self.var.set("")
            
    def get(self):
        """Get current entry value"""
        return self.var.get()

