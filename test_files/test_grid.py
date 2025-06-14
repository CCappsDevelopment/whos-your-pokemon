#!/usr/bin/env python3
"""
Test script to debug the grid layout issue
"""

import tkinter as tk

def create_test_grid():
    root = tk.Tk()
    root.title("Grid Test")
    root.geometry("800x600")
    root.configure(bg='#E3F2FD')
    
    # Main frame
    main_frame = tk.Frame(root, bg='#E3F2FD')
    main_frame.pack(expand=True, fill='both', padx=10, pady=10)
    
    # Title
    title = tk.Label(main_frame, text="Grid Test", font=('Arial', 20, 'bold'), bg='#E3F2FD')
    title.pack(pady=(0, 15))
    
    # Game frame
    game_frame = tk.Frame(main_frame, bg='#E3F2FD')
    game_frame.pack(expand=True, fill='both')
    
    # Configure columns
    game_frame.grid_columnconfigure(0, weight=1, minsize=300)  # Player 1
    game_frame.grid_columnconfigure(1, weight=0, minsize=20)   # Divider  
    game_frame.grid_columnconfigure(2, weight=1, minsize=300)  # Player 2
    game_frame.grid_rowconfigure(0, weight=1)
    
    # Player 1 container
    p1_container = tk.Frame(game_frame, bg='#E3F2FD')
    p1_container.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
    
    p1_label = tk.Label(p1_container, text="Player 1", font=('Arial', 16, 'bold'), 
                       bg='lightgreen', relief='solid', borderwidth=2)
    p1_label.pack(pady=(0, 5))
    
    # Player 1 grid
    p1_grid = tk.Frame(p1_container, bg='lightblue', relief='sunken', borderwidth=2)
    p1_grid.pack(expand=True, fill='both')
    
    # Create 4x6 grid of buttons for Player 1
    for row in range(4):
        for col in range(6):
            btn = tk.Button(p1_grid, text=f"P1-{row},{col}", width=8, height=2, 
                          font=('Arial', 8), bg='white')
            btn.grid(row=row, col=col, padx=1, pady=1, sticky='nsew')
    
    # Configure P1 grid
    for i in range(4):
        p1_grid.grid_rowconfigure(i, weight=1)
    for i in range(6):
        p1_grid.grid_columnconfigure(i, weight=1)
    
    # Divider
    divider = tk.Frame(game_frame, bg='red', width=5)
    divider.grid(row=0, column=1, sticky='ns')
    
    # Player 2 container
    p2_container = tk.Frame(game_frame, bg='#E3F2FD')
    p2_container.grid(row=0, column=2, sticky='nsew', padx=(5, 0))
    
    p2_label = tk.Label(p2_container, text="Player 2", font=('Arial', 16, 'bold'), 
                       bg='lightcoral', relief='solid', borderwidth=2)
    p2_label.pack(pady=(0, 5))
    
    # Player 2 grid
    p2_grid = tk.Frame(p2_container, bg='lightblue', relief='sunken', borderwidth=2)
    p2_grid.pack(expand=True, fill='both')
    
    # Create 4x6 grid of buttons for Player 2
    for row in range(4):
        for col in range(6):
            btn = tk.Button(p2_grid, text=f"P2-{row},{col}", width=8, height=2, 
                          font=('Arial', 8), bg='white')
            btn.grid(row=row, col=col, padx=1, pady=1, sticky='nsew')
    
    # Configure P2 grid
    for i in range(4):
        p2_grid.grid_rowconfigure(i, weight=1)
    for i in range(6):
        p2_grid.grid_columnconfigure(i, weight=1)
    
    # Control buttons
    control_frame = tk.Frame(main_frame, bg='#E3F2FD')
    control_frame.pack(pady=15)
    
    btn1 = tk.Button(control_frame, text="Button 1", font=('Arial', 14), 
                     bg='blue', fg='white', padx=20, pady=5)
    btn1.pack(side='left', padx=10)
    
    btn2 = tk.Button(control_frame, text="Button 2", font=('Arial', 14), 
                     bg='orange', fg='white', padx=20, pady=5)
    btn2.pack(side='left', padx=10)
    
    print("Test grid created successfully")
    root.mainloop()

if __name__ == "__main__":
    create_test_grid()
