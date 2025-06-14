"""
Base screen class for Pokemon Guess Game
"""
import tkinter as tk


class BaseScreen:
    """Base class for all game screens"""
    
    def __init__(self, root, game_instance):
        self.root = root
        self.game = game_instance
        self.container = None
    
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Unbind Enter key
        self.root.unbind('<Return>')
    
    def show(self):
        """Show this screen (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement show() method")
