#!/usr/bin/env python3
"""
Test autocomplete selection bug fix
"""

import tkinter as tk
import sys
import os

# Add current directory to path to import from main.py
sys.path.insert(0, os.path.dirname(__file__))

from main import AutocompleteEntry

def test_autocomplete_fix():
    """Test the autocomplete dropdown hiding fix"""
    root = tk.Tk()
    root.title("Autocomplete Selection Fix Test")
    root.geometry("400x300")
    root.configure(bg='#3d7dca')
    
    # Test data
    pokemon_names = ["Pikachu", "Pidgey", "Pidgeotto", "Pidgeot", "Piplup", "Prinplup"]
    
    # Title
    title_label = tk.Label(
        root,
        text="Test Autocomplete Selection Bug Fix",
        font=('Arial', 16, 'bold'),
        fg='#003a70',
        bg='#3d7dca'
    )
    title_label.pack(pady=20)
    
    # Instructions
    instruction_label = tk.Label(
        root,
        text="1. Type 'pi' to see suggestions\n2. Click on a suggestion\n3. Dropdown should disappear\n4. Start typing again to see dropdown reappear",
        font=('Arial', 11),
        fg='#222222',
        bg='#3d7dca',
        justify='left'
    )
    instruction_label.pack(pady=10)
    
    # Autocomplete widget
    autocomplete = AutocompleteEntry(
        root,
        values=pokemon_names,
        width=25
    )
    autocomplete.pack(pady=20)
    
    # Result display
    def show_selection():
        result_label.configure(text=f"Selected: {autocomplete.get()}")
    
    check_button = tk.Button(
        root,
        text="Show Selection",
        font=('Arial', 12),
        bg='#ffcb05',
        fg='#222222',
        command=show_selection,
        cursor='hand2'
    )
    check_button.pack(pady=10)
    
    result_label = tk.Label(
        root,
        text="Selected: None",
        font=('Arial', 12),
        fg='#222222',
        bg='#3d7dca'
    )
    result_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_autocomplete_fix()
