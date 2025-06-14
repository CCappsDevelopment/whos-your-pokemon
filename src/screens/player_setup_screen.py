"""
Player setup screen for Pokemon Guess Game
"""
import tkinter as tk
from tkinter import messagebox
from .base_screen import BaseScreen
from ..widgets import AutocompleteEntry


class PlayerSetupScreen(BaseScreen):
    """Screen for player name and Pokemon selection"""
    
    def show(self, player_num):
        """Setup screen for player selection"""
        self.clear_screen()
        
        # Main container
        self.container = tk.Frame(self.root, bg='#3d7dca')
        self.container.pack(expand=True, fill='both')
        
        # Logo
        logo_image = self.game.image_loader.load_logo_image('player-setup-logo.png', max_width=500, max_height=120)
        if logo_image:
            logo_label = tk.Label(
                self.container,
                image=logo_image,
                bg='#3d7dca'
            )
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(50, 10))
        else:
            # Fallback to text if logo doesn't load
            title_label = tk.Label(
                self.container,
                text="Player Setup",
                font=('Arial', 36, 'bold'),
                fg='#003a70',
                bg='#3d7dca'
            )
            title_label.pack(pady=(50, 10))
        
        # Player number indicator
        player_label = tk.Label(
            self.container,
            text=f"Player {player_num}",
            font=('Arial', 24, 'bold'),
            fg='#003a70',
            bg='#3d7dca'
        )
        player_label.pack(pady=(0, 30))
        
        # Name input
        name_label = tk.Label(
            self.container,
            text="Enter your name:",
            font=('Arial', 18),
            fg='#222222',
            bg='#3d7dca'
        )
        name_label.pack(pady=10)
        
        name_entry = tk.Entry(
            self.container,
            font=('Arial', 16),
            width=25,
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
            self.container,
            text="Choose your Pokémon (start typing to search):",
            font=('Arial', 18),
            fg='#222222',
            bg='#3d7dca'
        )
        pokemon_label.pack(pady=(30, 10))
        
        # Autocomplete entry for Pokemon selection
        pokemon_autocomplete = AutocompleteEntry(
            self.container,
            values=self.game.filtered_pokemon_list,
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
            
            # Validate that the chosen Pokemon exists in our filtered list
            if chosen_pokemon not in self.game.filtered_pokemon_list:
                messagebox.showerror("Error", f"'{chosen_pokemon}' is not a valid Pokémon from the selected generations. Please select from the suggestions.")
                return
            
            if player_num == 1:
                self.game.player1_name = name
                self.game.player1_chosen = chosen_pokemon
                self.game.setup_player(2)
            else:
                self.game.player2_name = name
                self.game.player2_chosen = chosen_pokemon
                self.game.create_game_screen()
        
        submit_button = tk.Button(
            self.container,
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
