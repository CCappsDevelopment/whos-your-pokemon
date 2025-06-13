#!/usr/bin/env python3
"""
Test script to verify specific fixes for autocomplete and grid buttons
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add current directory to path to import from main.py
sys.path.insert(0, os.path.dirname(__file__))

from main import AutocompleteEntry

def test_fixes():
    """Test the specific fixes requested"""
    root = tk.Tk()
    root.title("Fix Verification Test")
    root.geometry("500x400")
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
        text="Autocomplete & Grid Button Fix Test",
        font=('Arial', 16, 'bold'),
        fg='#1565C0',
        bg='#E3F2FD'
    )
    title_label.pack(pady=20)
    
    # Test 1: Autocomplete Visual Feedback
    test1_label = tk.Label(
        root,
        text="Test 1: Autocomplete should show cursor and highlight on focus",
        font=('Arial', 12),
        bg='#E3F2FD'
    )
    test1_label.pack(pady=(20, 5))
    
    autocomplete1 = AutocompleteEntry(
        root,
        values=pokemon_names,
        width=25
    )
    autocomplete1.pack(pady=10)
    
    # Test 2: Dropdown Selection
    test2_label = tk.Label(
        root,
        text="Test 2: Type 'pik' and select from dropdown - should populate textbox",
        font=('Arial', 12),
        bg='#E3F2FD'
    )
    test2_label.pack(pady=(20, 5))
    
    autocomplete2 = AutocompleteEntry(
        root,
        values=pokemon_names,
        width=25
    )
    autocomplete2.pack(pady=10)
    
    # Button to check selection
    def check_selection():
        selected = autocomplete2.get()
        if selected:
            messagebox.showinfo("Selection Test", f"✅ Selection works! Selected: {selected}")
        else:
            messagebox.showwarning("Selection Test", "❌ No selection made")
    
    check_button = tk.Button(
        root,
        text="Check Selection",
        font=('Arial', 12, 'bold'),
        bg='#3d7dca',
        fg='white',
        command=check_selection,
        cursor='hand2'
    )
    check_button.pack(pady=10)
    
    # Test 3: Button Grid Simulation
    test3_label = tk.Label(
        root,
        text="Test 3: Fixed-size buttons (should not change size when content changes)",
        font=('Arial', 12),
        bg='#E3F2FD'
    )
    test3_label.pack(pady=(20, 5))
    
    # Create a small grid of buttons to test sizing
    button_frame = tk.Frame(root, bg='#E3F2FD')
    button_frame.pack(pady=10)
    
    test_buttons = []
    for i in range(3):
        row_buttons = []
        for j in range(3):
            btn = tk.Button(
                button_frame,
                bg='#FFFFFF',
                fg='#333333',
                relief='raised',
                borderwidth=1,
                width=10,  # Fixed character width
                height=4,  # Fixed character height
                font=('Arial', 7, 'bold'),
                anchor='center',
                text=f"Btn{i}{j}",
                command=lambda r=i, c=j: toggle_test_button(r, c)
            )
            btn.grid(row=i, column=j, padx=2, pady=2)
            row_buttons.append(btn)
        test_buttons.append(row_buttons)
    
    # Configure grid weights
    for i in range(3):
        button_frame.grid_rowconfigure(i, weight=1, uniform="row")
        button_frame.grid_columnconfigure(i, weight=1, uniform="col")
    
    def toggle_test_button(row, col):
        """Toggle button content to test size consistency"""
        btn = test_buttons[row][col]
        current_text = btn.cget("text")
        
        if current_text.startswith("Btn"):
            # Change to X
            btn.configure(
                text="X",
                bg='#F44336',
                fg='white',
                font=('Arial', 20, 'bold'),
                width=10,  # Keep same size
                height=4   # Keep same size
            )
        else:
            # Change back to original
            btn.configure(
                text=f"Btn{row}{col}",
                bg='#FFFFFF',
                fg='#333333',
                font=('Arial', 7, 'bold'),
                width=10,  # Keep same size
                height=4   # Keep same size
            )
    
    # Instructions
    instruction_label = tk.Label(
        root,
        text="Click grid buttons to toggle X - size should remain constant",
        font=('Arial', 10),
        bg='#E3F2FD',
        fg='#666'
    )
    instruction_label.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_fixes()
