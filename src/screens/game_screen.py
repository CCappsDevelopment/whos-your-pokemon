"""
Main game screen for Pokemon Guess Game
"""
import tkinter as tk
from tkinter import ttk, messagebox
from .base_screen import BaseScreen


class GameScreen(BaseScreen):
    """Main game interface screen"""
    
    def show(self):
        """Create the main game interface"""
        self.clear_screen()
        self.game.game_active = True
        
        # Generate grids
        self.game.generate_grids()
        
        # Main container
        self.game.main_frame = tk.Frame(self.root, bg='#3d7dca')
        self.game.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Logo
        logo_image = self.game.image_loader.load_logo_image('whos-your-pokemon-logo.png', max_width=400, max_height=80)
        if logo_image:
            logo_label = tk.Label(
                self.game.main_frame,
                image=logo_image,
                bg='#3d7dca'
            )
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(0, 10))
        else:
            # Fallback to text if logo doesn't load
            title_label = tk.Label(
                self.game.main_frame,
                text="Who's Your Pokémon!",
                font=('Arial', 22, 'bold'),
                fg='#003a70',
                bg='#3d7dca'
            )
            title_label.pack(pady=(0, 10))
        
        # Create horizontal layout using pack with equal distribution
        game_frame = tk.Frame(self.game.main_frame, bg='#3d7dca')
        game_frame.pack(expand=True, fill='both')
        
        # Player 1 side (LEFT) - width for 96x96 images
        player1_frame = tk.Frame(game_frame, bg='#3d7dca', width=450)
        player1_frame.pack(side='left', expand=True, fill='both', padx=(0, 2))
        player1_frame.pack_propagate(False)  # Maintain width
        
        # Remove "(Player 1)" suffix and increase font size by 25% (14 -> 17.5, rounded to 18)
        self.game.player1_name_label = tk.Label(
            player1_frame,
            text=f"{self.game.player1_name}",
            font=('Arial', 18, 'bold'),
            bg='lightgreen',
            relief='solid',
            borderwidth=2,
            padx=10,
            pady=15
        )
        self.game.player1_name_label.pack(pady=(0, 5))
        
        self.game.player1_remaining_label = tk.Label(
            player1_frame,
            text="Remaining: 24",
            font=('Arial', 11),
            bg='#3d7dca'
        )
        self.game.player1_remaining_label.pack(pady=(0, 5))
        
        # Player 1 grid container - remove red border
        p1_grid_container = tk.Frame(player1_frame, bg='#3d7dca', relief='solid', borderwidth=1)
        p1_grid_container.pack(expand=True, fill='both', pady=(0, 10))
        
        p1_grid_frame = tk.Frame(p1_grid_container, bg='#3d7dca')
        p1_grid_frame.pack(expand=True, fill='both', padx=3, pady=3)
        
        print("About to create Player 1 grid...")
        self.create_grid(p1_grid_frame, 1)
        
        # Player 2 side (RIGHT) - width for 96x96 images
        player2_frame = tk.Frame(game_frame, bg='#3d7dca', width=450)
        player2_frame.pack(side='right', expand=True, fill='both', padx=(2, 0))
        player2_frame.pack_propagate(False)  # Maintain width
        
        # Remove "(Player 2)" suffix and increase font size by 25% (14 -> 17.5, rounded to 18)
        self.game.player2_name_label = tk.Label(
            player2_frame,
            text=f"{self.game.player2_name}",
            font=('Arial', 18, 'bold'),
            bg='#E3F2FD',
            relief='solid',
            borderwidth=2,
            padx=10,
            pady=15
        )
        self.game.player2_name_label.pack(pady=(0, 5))
        
        self.game.player2_remaining_label = tk.Label(
            player2_frame,
            text="Remaining: 24",
            font=('Arial', 11),
            bg='#3d7dca'
        )
        self.game.player2_remaining_label.pack(pady=(0, 5))
        
        # Player 2 grid container - remove red border
        p2_grid_container = tk.Frame(player2_frame, bg='#3d7dca', relief='solid', borderwidth=1)
        p2_grid_container.pack(expand=True, fill='both', pady=(0, 10))
        
        p2_grid_frame = tk.Frame(p2_grid_container, bg='#3d7dca')
        p2_grid_frame.pack(expand=True, fill='both', padx=3, pady=3)
        
        print("About to create Player 2 grid...")
        self.create_grid(p2_grid_frame, 2)
        
        # Control buttons at the bottom
        control_frame = tk.Frame(self.game.main_frame, bg='#3d7dca')
        control_frame.pack(pady=10)
        
        self.game.end_turn_button = tk.Button(
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
            command=self.game.end_turn
        )
        self.game.end_turn_button.pack(side='left', padx=10)
        
        self.game.guess_button = tk.Button(
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
            command=self.game.make_guess
        )
        self.game.guess_button.pack(side='left', padx=10)
        
        # Set initial turn
        self.game.update_turn_indicator()
        print("Game screen layout complete. Updating turn indicator...")
        print("Game screen creation finished!")
    
    def create_grid(self, parent, player):
        """Create a 6x4 grid of Pokemon buttons with uniform sizing"""
        grid_data = self.game.player1_grid if player == 1 else self.game.player2_grid
        button_list = []
        
        # Debug print to ensure this method is called
        print(f"Creating grid for player {player} with {len(grid_data)} Pokemon")
        
        # Fixed button size for uniform grid - 96px image + 4px padding (2px each side)
        button_size = 100  # 96px image + 4px padding
        
        for row in range(4):
            button_row = []
            for col in range(6):
                pokemon_index = row * 6 + col
                if pokemon_index < len(grid_data):
                    pokemon_name = grid_data[pokemon_index]
                    
                    # Create button with exact size
                    button = tk.Button(
                        parent,
                        text="",  # No text, image only
                        width=button_size,
                        height=button_size,
                        relief='solid',
                        borderwidth=2,
                        bg='#cccccc',
                        activebackground='#999999',
                        command=lambda p=pokemon_name, target_player=player: self.game.toggle_pokemon(p, target_player)
                    )
                    
                    # Position button in grid
                    button.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
                    
                    # Load and set Pokemon image
                    sprite_url = self.game.data_manager.get_pokemon_sprite_url(pokemon_name)
                    if sprite_url:
                        image = self.game.image_loader.download_and_cache_image(pokemon_name, sprite_url)
                        if image:
                            button.configure(image=image)
                            button.image = image  # Keep reference
                    
                    # Store button with Pokemon name for later reference
                    button.pokemon_name = pokemon_name
                    button_row.append(button)
                    
                    print(f"Created button for {pokemon_name} at ({row}, {col})")
                else:
                    button_row.append(None)
            
            button_list.append(button_row)
        
        # Configure grid weights for equal distribution
        for i in range(4):  # 4 rows
            parent.grid_rowconfigure(i, weight=1)
        for i in range(6):  # 6 columns
            parent.grid_columnconfigure(i, weight=1)
        
        # Store button references
        if player == 1:
            self.game.player1_buttons = button_list
        else:
            self.game.player2_buttons = button_list
        
        print(f"Player {player} buttons stored: {len(button_list)} rows")
