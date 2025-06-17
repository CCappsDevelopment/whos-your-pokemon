"""
Main Pokemon Guess Game class - Complete Version
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random

from ..data import PokemonDataManager
from ..utils import ImageLoader
from ..screens import (
    StartupScreen, GameSettingsScreen, PlayerSetupScreen, 
    GameScreen, GameOverScreen, PokemonGridSetupScreen
)


class PokemonGuessGame:
    """Main game controller class"""
    
    def __init__(self):
        # Initialize data and utilities
        self.data_manager = PokemonDataManager()
        self.image_loader = ImageLoader()
        
        # Game state
        self.player1_name = ""
        self.player2_name = ""
        self.player1_chosen = ""
        self.player2_chosen = ""
        self.current_player = 1
        self.game_active = False
        
        # Generation selection
        self.selected_generations = set(['1', '2', '3', '4', '5', '6', '7', '8', '9'])  # All selected by default
        self.generation_vars = {}
        self.all_regions_var = None
        self.filtered_pokemon_list = []
        
        # Variant handling - initialize with all variants selected by default
        self.variant_vars = {}
        self.selected_variants = set()
        self.all_variants_var = None
        self.pokemon_selection_var = None
        
        # Initialize selected_variants with all available variants
        self._initialize_default_variants()
        
        # Grid data
        self.player1_grid = []
        self.player2_grid = []
        self.player1_buttons = []
        self.player2_buttons = []
        self.player1_eliminated = set()
        self.player2_eliminated = set()
        
        # Manual selection state
        self.manual_selection_grids = {}  # Store manually selected grids
        self.current_setup_player = 1  # Track which player is setting up their grid
        
        # UI components
        self.root = None
        self.main_frame = None
        self.player1_name_label = None
        self.player2_name_label = None
        self.player1_remaining_label = None
        self.player2_remaining_label = None
        self.confirm_button = None
        self.end_turn_button = None
        self.guess_button = None
        
        # Initialize screens
        self.startup_screen = None
        self.generation_screen = None
        self.player_setup_screen = None
        self.pokemon_grid_setup_screen = None
        self.game_screen = None
        self.game_over_screen = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main UI window"""
        self.root = tk.Tk()
        self.root.title("Who's Your Pokémon!")
        
        # Set window to fullscreen by default
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#3d7dca')
        
        # Allow escape key to close the window and F11 to toggle fullscreen
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.bind('<F11>', self.toggle_fullscreen)
        
        # Load X icon after root window is created
        self.image_loader.load_x_icon()
        
        # Initialize all screens
        self.startup_screen = StartupScreen(self.root, self)
        self.generation_screen = GameSettingsScreen(self.root, self)
        self.player_setup_screen = PlayerSetupScreen(self.root, self)
        self.pokemon_grid_setup_screen = PokemonGridSetupScreen(self.root, self)
        self.game_screen = GameScreen(self.root, self)
        self.game_over_screen = GameOverScreen(self.root, self)
        
        # Initialize the filtered Pokemon list with default settings (all generations/variants)
        self.update_filtered_pokemon_list()
        
        self.show_startup_screen()
    
    def show_startup_screen(self):
        """Display the initial startup screen"""
        self.startup_screen.show()
    
    def start_game(self):
        """Begin the game setup process - go directly to player setup"""
        self.setup_player(1)
    
    def show_settings(self):
        """Display the game settings screen"""
        self.generation_screen.show()
    
    def return_to_startup(self):
        """Return to the startup screen"""
        self.show_startup_screen()
    
    def show_generation_selection(self):
        """Display the generation selection screen"""
        self.generation_screen.show()
    
    def setup_player(self, player_num):
        """Setup screen for player selection"""
        # Before showing player setup, check if we need manual grid selection
        selection_method = self.pokemon_selection_var.get() if self.pokemon_selection_var else "randomize"
        
        if selection_method == "manual":
            # If manual selection, first do the Pokemon choice, then grid setup
            if player_num == 1 and not self.player1_chosen:
                # Player 1 needs to choose their Pokemon first
                self.player_setup_screen.show(player_num)
            elif player_num == 1 and self.player1_chosen and player_num not in self.manual_selection_grids:
                # Player 1 has chosen Pokemon, now set up grid
                self.setup_player_grid(player_num)
            elif player_num == 2 and not self.player2_chosen:
                # Player 2 needs to choose their Pokemon first
                self.player_setup_screen.show(player_num)
            elif player_num == 2 and self.player2_chosen and player_num not in self.manual_selection_grids:
                # Player 2 has chosen Pokemon, now set up grid
                self.setup_player_grid(player_num)
            else:
                # Both players done, start game
                self.start_main_game()
        else:
            # Regular randomized flow
            self.player_setup_screen.show(player_num)
    
    def setup_player_grid(self, player_num):
        """Show manual grid setup screen for a player"""
        self.current_setup_player = player_num
        
        # Get player name and chosen Pokemon
        if player_num == 1:
            player_name = self.player1_name
            chosen_pokemon = self.player1_chosen
        else:
            player_name = self.player2_name
            chosen_pokemon = self.player2_chosen
        
        self.pokemon_grid_setup_screen.show(player_num, player_name, chosen_pokemon)
    
    def complete_player_grid_setup(self, player_num, selected_grid):
        """Complete manual grid setup for a player and proceed to next step"""
        # Store the manually selected grid
        self.manual_selection_grids[player_num] = selected_grid
        print(f"🎮 Player {player_num} completed manual grid setup with {len(selected_grid)} Pokemon")
        
        if player_num == 1:
            # Player 1 finished, move to Player 2 setup
            self.setup_player(2)
        else:
            # Player 2 finished, start the main game
            self.start_main_game()
    
    def start_main_game(self):
        """Start the main game with manually selected grids or generate random grids"""
        selection_method = self.pokemon_selection_var.get() if self.pokemon_selection_var else "randomize"
        
        if selection_method == "manual" and self.manual_selection_grids:
            # Use manually selected grids
            self.player1_grid = self.manual_selection_grids.get(1, [])
            self.player2_grid = self.manual_selection_grids.get(2, [])
            print(f"🎮 Using manual grids - P1: {len(self.player1_grid)} Pokemon, P2: {len(self.player2_grid)} Pokemon")
        else:
            # Generate random grids as before
            self.generate_grids()
        
        # Reset game state
        self.player1_eliminated = set()
        self.player2_eliminated = set()
        self.current_player = 1
        self.game_active = True
        
        # Create and show the game screen
        self.create_game_screen()
    
    def create_game_screen(self):
        """Create the main game interface"""
        self.game_screen.show()
    
    def generate_grids(self):
        """Generate the Pokemon grids for both players (only if not already set by manual selection)"""
        print(f"Generating grids. Player 1 chose: {self.player1_chosen}, Player 2 chose: {self.player2_chosen}")
        
        # Only generate grids if they haven't been manually set
        if not self.player1_grid:
            # Create Player 1's grid - select 24 random Pokémon from the filtered list
            available_pokemon = self.filtered_pokemon_list.copy()
            
            # Ensure Player 1's chosen Pokemon is included
            if self.player1_chosen in available_pokemon:
                available_pokemon.remove(self.player1_chosen)
            
            # Select 23 random Pokemon and add the chosen one
            self.player1_grid = random.sample(available_pokemon, 23)
            self.player1_grid.append(self.player1_chosen)
            random.shuffle(self.player1_grid)
        
        if not self.player2_grid:
            # Create Player 2's grid - select 24 random Pokémon from the filtered list
            available_pokemon = self.filtered_pokemon_list.copy()
            
            # Ensure Player 2's chosen Pokemon is included
            if self.player2_chosen in available_pokemon:
                available_pokemon.remove(self.player2_chosen)
            
            # Select 23 random Pokemon and add the chosen one
            self.player2_grid = random.sample(available_pokemon, 23)
            self.player2_grid.append(self.player2_chosen)
            random.shuffle(self.player2_grid)
        
        print(f"Player 1 grid: {self.player1_grid[:6]}...")  # Show first 6
        print(f"Player 2 grid: {self.player2_grid[:6]}...")  # Show first 6
    
    def toggle_pokemon(self, pokemon, target_player_grid):
        """Toggle elimination of a Pokemon from the current player's perspective"""
        if not self.game_active:
            return
        
        # The current player is clicking on their opponent's grid
        # We need to update the elimination status from the current player's perspective
        # But update the visual on the target grid
        
        if self.current_player == 1:
            # Player 1 is clicking, so update player 1's eliminated set
            eliminated_set = self.player1_eliminated
        else:
            # Player 2 is clicking, so update player 2's eliminated set
            eliminated_set = self.player2_eliminated
        
        # Get the buttons for the target grid (the one being clicked)
        if target_player_grid == 1:
            buttons = self.player1_buttons
        else:
            buttons = self.player2_buttons
        
        # Toggle elimination status
        if pokemon in eliminated_set:
            eliminated_set.remove(pokemon)
        else:
            eliminated_set.add(pokemon)
        
        # Update the visual representation on the target grid
        for row in buttons:
            for tile in row:
                if tile and hasattr(tile, 'pokemon_name') and tile.pokemon_name == pokemon:
                    if pokemon in eliminated_set:
                        # Show X overlay on the image label
                        if self.image_loader.x_icon:
                            tile.image_label.configure(image=self.image_loader.x_icon)
                            tile.image_label.image = self.image_loader.x_icon
                    else:
                        # Restore original image on the image label
                        sprite_url = self.data_manager.get_pokemon_sprite_url(pokemon)
                        if sprite_url:
                            image = self.image_loader.load_pokemon_image(pokemon, sprite_url)
                            if image:
                                tile.image_label.configure(image=image)
                                tile.image_label.image = image
        
        self.update_remaining_count()
    
    def update_remaining_count(self):
        """Update the remaining Pokemon count"""
        remaining1 = 24 - len(self.player1_eliminated)
        remaining2 = 24 - len(self.player2_eliminated)
        
        if self.player1_remaining_label:
            self.player1_remaining_label.configure(text=f"Remaining: {remaining1}")
        if self.player2_remaining_label:
            self.player2_remaining_label.configure(text=f"Remaining: {remaining2}")
    
    def update_turn_indicator(self):
        """Update visual indication of current player"""
        if self.player1_name_label and self.player2_name_label:
            if self.current_player == 1:
                self.player1_name_label.configure(bg='#4CAF50', fg='white')
                self.player2_name_label.configure(bg='#E3F2FD', fg='#333')
            else:
                self.player1_name_label.configure(bg='#E3F2FD', fg='#333')
                self.player2_name_label.configure(bg='#4CAF50', fg='white')
        
        # Update grid clickability based on current turn
        if self.game_screen and hasattr(self.game_screen, 'update_grid_clickability'):
            self.game_screen.update_grid_clickability()
    
    def end_turn(self):
        """End current player's turn"""
        if not self.game_active:
            return
        
        # Check if current player eliminated opponent's chosen Pokemon
        opponent_chosen = self.player2_chosen if self.current_player == 1 else self.player1_chosen
        current_player_eliminated = self.player1_eliminated if self.current_player == 1 else self.player2_eliminated
        
        if opponent_chosen in current_player_eliminated:
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
        
        # Get available Pokemon from opponent's grid (non-eliminated from current player's perspective)
        opponent_grid = self.player2_grid if self.current_player == 1 else self.player1_grid
        # Use current player's eliminated set - this represents what THEY have crossed out
        current_player_eliminated = self.player1_eliminated if self.current_player == 1 else self.player2_eliminated
        available_pokemon = [p for p in opponent_grid if p not in current_player_eliminated]
        
        if not available_pokemon:
            messagebox.showwarning("No Pokemon Available", "All Pokemon have been eliminated!")
            return
        
        # Create guess dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Make Your Guess")
        dialog.geometry("400x200")
        dialog.configure(bg='#3d7dca')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        tk.Label(
            dialog,
            text=f"{current_player_name}, choose your guess:",
            font=('Arial', 16, 'bold'),
            fg='#222222',
            bg='#3d7dca'
        ).pack(pady=20)
        
        # Dropdown for available Pokemon
        guess_var = tk.StringVar()
        guess_dropdown = ttk.Combobox(
            dialog,
            textvariable=guess_var,
            values=sorted(available_pokemon),
            state="readonly",
            font=('Arial', 14),
            width=20
        )
        
        # Custom style for the dropdown
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
        self.game_over_screen = GameOverScreen(self.root, self)
        self.game_over_screen.show(result, message)
    
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
        
        # Reset manual selection state
        self.manual_selection_grids = {}
        self.current_setup_player = 1
        
        # Show startup screen
        self.show_startup_screen()

    def update_selected_generations(self):
        """Update the selected generations set based on checkbox states"""
        self.selected_generations.clear()
        for gen, var in self.generation_vars.items():
            if var.get():
                self.selected_generations.add(gen)
        
        # Update filtered Pokémon list
        self.update_filtered_pokemon_list()
        print(f"📊 Selected generations: {len(self.selected_generations)} generations")
    
    def on_all_regions_changed(self):
        """Handle All Regions checkbox change"""
        if self.all_regions_var.get():
            # Select all generations
            for var in self.generation_vars.values():
                var.set(True)
        else:
            # Deselect all generations
            for var in self.generation_vars.values():
                var.set(False)
        
        self.update_selected_generations()
        self.update_confirm_button_state()
    
    def on_generation_changed(self):
        """Handle individual generation checkbox change"""
        # Check if all generations are selected
        all_selected = all(var.get() for var in self.generation_vars.values())
        
        # Update All Regions checkbox accordingly
        self.all_regions_var.set(all_selected)
        
        self.update_selected_generations()
        self.update_confirm_button_state()
    
    def update_confirm_button_state(self):
        """Enable/disable confirm button based on selection and pokemon selection method"""
        has_generation_selection = any(var.get() for var in self.generation_vars.values())
        selection_method = self.pokemon_selection_var.get() if self.pokemon_selection_var else "randomize"
        
        # Button should be enabled if there's a generation selection
        should_enable = has_generation_selection
        
        if self.confirm_button:
            if should_enable:
                self.confirm_button.config(state='normal', bg='#ffcb05')
            else:
                self.confirm_button.config(state='disabled', bg='#cccccc')
    
    def update_selected_variants(self):
        """Update the selected variants set based on checkbox states"""
        self.selected_variants.clear()
        for variant, var in self.variant_vars.items():
            if var.get():
                self.selected_variants.add(variant)
        
        # Update filtered Pokémon list based on both generations and variants
        self.update_filtered_pokemon_list()
        print(f"🔮 Selected variants: {len(self.selected_variants)} variant types")
    
    def on_all_variants_changed(self):
        """Handle All Variants checkbox change"""
        if self.all_variants_var.get():
            # Select all variants
            for var in self.variant_vars.values():
                var.set(True)
        else:
            # Deselect all variants
            for var in self.variant_vars.values():
                var.set(False)
        
        self.update_selected_variants()
        self.update_confirm_button_state()
    
    def on_variant_changed(self):
        """Handle individual variant checkbox change"""
        # Check if all variants are selected
        all_selected = all(var.get() for var in self.variant_vars.values())
        
        # Update All Variants checkbox accordingly
        self.all_variants_var.set(all_selected)
        
        self.update_selected_variants()
        self.update_confirm_button_state()
    
    def on_pokemon_selection_changed(self, event=None):
        """Handle Pokemon selection method change"""
        selection_method = self.pokemon_selection_var.get() if self.pokemon_selection_var else "randomize"
        print(f"🎯 Pokemon selection method changed to: {selection_method}")
        
        # Update confirm button state for both manual and randomize
        self.update_confirm_button_state()
    
    def update_filtered_pokemon_list(self):
        """Update filtered Pokemon list based on both generations and variants"""
        # This will be called by both generation and variant update methods
        self.filtered_pokemon_list = self.data_manager.filter_pokemon_by_settings(
            self.selected_generations, 
            self.selected_variants
        )
        print(f"📊 Filtered to {len(self.filtered_pokemon_list)} Pokémon")
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
        
        # If exiting fullscreen, set a reasonable window size and center it
        if current_state:
            self.root.geometry("1300x800")
            # Center the window when exiting fullscreen
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        """Start the game"""
        self.root.mainloop()

    def _initialize_default_variants(self):
        """Initialize selected_variants with all available variants by default"""
        try:
            # Get all unique variants from the Pokemon data
            all_variants = set()
            for pokemon_name, pokemon_info in self.data_manager.pokemon_data.items():
                if isinstance(pokemon_info, dict):
                    variant = pokemon_info.get('variant')
                    if variant:
                        all_variants.add(variant)
            
            # Add all variants to selected_variants (default behavior: all variants enabled)
            self.selected_variants = all_variants.copy()
            print(f"🔮 Initialized with {len(self.selected_variants)} default variants")
            
        except Exception as e:
            print(f"⚠️ Error initializing default variants: {e}")
            # Fallback: empty set (no variants selected)
            self.selected_variants = set()
