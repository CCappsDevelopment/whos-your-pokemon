"""
Main Pokemon Guess Game class
"""
import tkinter as tk
from tkinter import ttk, messagebox
import random

from ..data import PokemonDataManager
from ..utils import ImageLoader
from ..screens import (
    StartupScreen, GameSettingsScreen, PlayerSetupScreen, 
    GameScreen, GameOverScreen
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
        
        # Variant handling
        self.variant_vars = {}
        self.selected_variants = set()
        self.all_variants_var = None
        self.pokemon_selection_var = None
        
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
        self.confirm_button = None
        self.end_turn_button = None
        self.guess_button = None
        
        # Initialize screens
        self.startup_screen = None
        self.generation_screen = None
        self.player_setup_screen = None
        self.game_screen = None
        self.game_over_screen = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the main UI window"""
        self.root = tk.Tk()
        self.root.title("Who's Your Pokémon!")
        
        # Window size for 96x96 images with 100px buttons (6x4 grid)
        self.root.geometry("1300x800")
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
        self.image_loader.load_x_icon()
        
        # Initialize all screens
        self.startup_screen = StartupScreen(self.root, self)
        self.generation_screen = GameSettingsScreen(self.root, self)
        self.player_setup_screen = PlayerSetupScreen(self.root, self)
        self.game_screen = GameScreen(self.root, self)
        self.game_over_screen = GameOverScreen(self.root, self)
        
        self.show_startup_screen()
    
    def show_startup_screen(self):
        """Display the initial startup screen"""
        self.startup_screen.show()
    
    def start_game(self):
        """Begin the game setup process"""
        self.show_generation_selection()
    
    def show_generation_selection(self):
        """Display the generation selection screen"""
        self.generation_screen.show()
    
    def setup_player(self, player_num):
        """Setup screen for player selection"""
        self.player_setup_screen.show(player_num)
    
    def create_game_screen(self):
        """Create the main game interface"""
        self.game_screen.show()
    
    def generate_grids(self):
        """Generate the Pokemon grids for both players"""
        print(f"Generating grids. Player 1 chose: {self.player1_chosen}, Player 2 chose: {self.player2_chosen}")
        
        # Create Player 1's grid - select 24 random Pokémon from the filtered list
        available_pokemon = self.filtered_pokemon_list.copy()
        
        # Ensure Player 1's chosen Pokemon is included
        if self.player1_chosen in available_pokemon:
            available_pokemon.remove(self.player1_chosen)
        
        # Select 23 random Pokemon and add the chosen one
        self.player1_grid = random.sample(available_pokemon, 23)
        self.player1_grid.append(self.player1_chosen)
        random.shuffle(self.player1_grid)
        
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
            for button in row:
                if button and hasattr(button, 'pokemon_name') and button.pokemon_name == pokemon:
                    if pokemon in eliminated_set:
                        # Show X overlay
                        if self.image_loader.x_icon:
                            button.configure(image=self.image_loader.x_icon)
                            button.image = self.image_loader.x_icon
                    else:
                        # Restore original image
                        sprite_url = self.data_manager.get_pokemon_sprite_url(pokemon)
                        if sprite_url:
                            image = self.image_loader.download_and_cache_image(pokemon, sprite_url)
                            if image:
                                button.configure(image=image)
                                button.image = image
        
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
        
        # Button should be enabled if there's a generation selection and selection method is randomize
        should_enable = has_generation_selection and selection_method == "randomize"
        
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
        selection_method = self.pokemon_selection_var.get()
        
        # Disable continue button if manual is selected (not yet implemented)
        if selection_method == "manual":
            if self.confirm_button:
                self.confirm_button.config(state='disabled', bg='#cccccc')
                messagebox.showinfo("Feature Coming Soon", 
                                  "Manual Pokemon selection is not yet implemented. Please use 'randomize' for now.")
                self.pokemon_selection_var.set("randomize")
        
        self.update_confirm_button_state()
    
    def update_filtered_pokemon_list(self):
        """Update filtered Pokemon list based on both generations and variants"""
        # This will be called by both generation and variant update methods
        self.filtered_pokemon_list = self.data_manager.filter_pokemon_by_settings(
            self.selected_generations, 
            self.selected_variants
        )
        print(f"📊 Filtered to {len(self.filtered_pokemon_list)} Pokémon")
    
    def run(self):
        """Start the game"""
        self.root.mainloop()
