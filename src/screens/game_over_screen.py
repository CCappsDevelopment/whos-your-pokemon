"""
Game over screen for Pokemon Guess Game
"""
import tkinter as tk
from .base_screen import BaseScreen


class GameOverScreen(BaseScreen):
    """End game results screen"""
    
    def show(self, result, message):
        """End the game and show results"""
        self.game.game_active = False
        self.clear_screen()
        
        # Main container
        self.container = tk.Frame(self.root, bg='#3d7dca')
        self.container.pack(expand=True, fill='both')
        
        # Game Over Logo
        logo_image = self.game.image_loader.load_logo_image('game-over-logo.png', max_width=500, max_height=120)
        if logo_image:
            logo_label = tk.Label(
                self.container,
                image=logo_image,
                bg='#3d7dca'
            )
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(50, 20))
        
        # Result
        result_label = tk.Label(
            self.container,
            text=result,
            font=('Arial', 48, 'bold'),
            fg='#4CAF50' if 'Wins' in result else '#F44336',
            bg='#3d7dca'
        )
        result_label.pack(pady=(20, 20))
        
        # Message
        message_label = tk.Label(
            self.container,
            text=message,
            font=('Arial', 18),
            fg='#222222',
            bg='#3d7dca'
        )
        message_label.pack(pady=20)
        
        # New game button
        new_game_button = tk.Button(
            self.container,
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
            command=self.game.new_game,
            cursor='hand2'
        )
        new_game_button.pack(pady=40)
