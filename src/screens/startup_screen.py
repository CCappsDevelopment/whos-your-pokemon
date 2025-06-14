"""
Startup screen for Pokemon Guess Game
"""
import tkinter as tk
from .base_screen import BaseScreen


class StartupScreen(BaseScreen):
    """Initial startup screen with start button"""
    
    def show(self):
        """Display the initial startup screen"""
        self.clear_screen()
        
        # Main container
        self.container = tk.Frame(self.root, bg='#3d7dca')
        self.container.pack(expand=True, fill='both')
        
        # Logo
        logo_image = self.game.image_loader.load_logo_image('whos-your-pokemon-logo.png', max_width=600, max_height=200)
        if logo_image:
            logo_label = tk.Label(
                self.container,
                image=logo_image,
                bg='#3d7dca'
            )
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(100, 50))
        else:
            # Fallback to text if logo doesn't load
            title_label = tk.Label(
                self.container,
                text="Who's Your Pokémon!",
                font=('Arial', 48, 'bold'),
                fg='#003a70',
                bg='#3d7dca'
            )
            title_label.pack(pady=(100, 50))
        
        # Start button with rounded corners
        start_button = tk.Button(
            self.container,
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
            command=self.game.start_game,
            cursor='hand2'
        )
        start_button.pack(pady=20)
