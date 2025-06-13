#!/usr/bin/env python3
"""
Simple test for AutocompleteEntry widget
"""

import tkinter as tk
import sys
import os

# Add current directory to path to import from main.py
sys.path.insert(0, os.path.dirname(__file__))

from main import AutocompleteEntry

def test_autocomplete():
    """Test the autocomplete widget"""
    root = tk.Tk()
    root.title("Autocomplete Test")
    root.geometry("400x300")
    root.configure(bg='#E3F2FD')
    
    # Test data
    pokemon_names = [
        "Pikachu", "Bulbasaur", "Charmander", "Squirtle", "Caterpie", "Weedle",
        "Pidgey", "Rattata", "Spearow", "Ekans", "Sandshrew", "Nidoran♀",
        "Nidoran♂", "Clefairy", "Vulpix", "Jigglypuff", "Zubat", "Oddish",
        "Paras", "Venonat", "Diglett", "Meowth", "Psyduck", "Mankey"
    ]
    
    # Title
    title_label = tk.Label(
        root,
        text="Test Autocomplete Widget",
        font=('Arial', 18, 'bold'),
        fg='#1565C0',
        bg='#E3F2FD'
    )
    title_label.pack(pady=20)
    
    # Instructions
    instruction_label = tk.Label(
        root,
        text="Start typing a Pokémon name and select from dropdown:",
        font=('Arial', 12),
        bg='#E3F2FD'
    )
    instruction_label.pack(pady=10)
    
    # Autocomplete widget
    autocomplete = AutocompleteEntry(
        root,
        values=pokemon_names,
        width=25
    )
    autocomplete.pack(pady=20)
    
    # Button to test selection
    def test_selection():
        selected = autocomplete.get()
        result_label.configure(text=f"Selected: {selected}")
    
    test_button = tk.Button(
        root,
        text="Get Selection",
        font=('Arial', 12, 'bold'),
        bg='#3d7dca',
        fg='white',
        command=test_selection,
        cursor='hand2'
    )
    test_button.pack(pady=10)
    
    # Result display
    result_label = tk.Label(
        root,
        text="Selected: None",
        font=('Arial', 12),
        bg='#E3F2FD'
    )
    result_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_autocomplete()
