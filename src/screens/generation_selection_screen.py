"""
Generation selection screen for Pokemon Guess Game
"""
import tkinter as tk
from tkinter import messagebox
from .base_screen import BaseScreen


class GenerationSelectionScreen(BaseScreen):
    """Screen for selecting Pokemon generations"""
    
    def show(self):
        """Display the generation selection screen"""
        self.clear_screen()
        
        # Main container
        self.container = tk.Frame(self.root, bg='#3d7dca')
        self.container.pack(expand=True, fill='both')
        
        # Logo
        logo_image = self.game.image_loader.load_logo_image('select-generations-logo.png', max_width=600, max_height=120)
        if logo_image:
            logo_label = tk.Label(
                self.container,
                image=logo_image,
                bg='#3d7dca'
            )
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(50, 30))
        else:
            # Fallback to text if logo doesn't load
            title_label = tk.Label(
                self.container,
                text="Select Pokémon Generations",
                font=('Arial', 36, 'bold'),
                fg='#003a70',
                bg='#3d7dca'
            )
            title_label.pack(pady=(50, 30))
        
        # Subtitle
        subtitle_label = tk.Label(
            self.container,
            text="Choose which generations to include in your game:",
            font=('Arial', 16),
            fg='#222222',
            bg='#3d7dca'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Checkbox frame
        checkbox_frame = tk.Frame(self.container, bg='#3d7dca')
        checkbox_frame.pack(pady=20)
        
        # Generation data with regions
        generation_data = [
            ('1', 'I - Kanto'),
            ('2', 'II - Johto'),
            ('3', 'III - Hoenn'),
            ('4', 'IV - Sinnoh'),
            ('5', 'V - Unova'),
            ('6', 'VI - Kalos'),
            ('7', 'VII - Alola'),
            ('8', 'VIII - Galar'),
            ('9', 'IX - Paldea')
        ]
        
        # All Regions checkbox (first row)
        all_regions_frame = tk.Frame(checkbox_frame, bg='#3d7dca')
        all_regions_frame.pack(pady=(0, 10))
        
        self.game.all_regions_var = tk.BooleanVar(value=True)
        all_regions_cb = tk.Checkbutton(
            all_regions_frame,
            text="All Regions",
            variable=self.game.all_regions_var,
            font=('Arial', 16, 'bold'),
            fg='#003a70',
            bg='#3d7dca',
            selectcolor='#cccccc',
            activebackground='#3d7dca',
            activeforeground='#003a70',
            command=self.game.on_all_regions_changed
        )
        all_regions_cb.pack()
        
        # Individual generation checkboxes (in 3x3 grid with proper alignment)
        grid_frame = tk.Frame(checkbox_frame, bg='#3d7dca')
        grid_frame.pack(pady=10)
        
        # Configure grid columns for consistent alignment
        for col in range(3):
            grid_frame.grid_columnconfigure(col, weight=1, uniform="checkbox_col")
        
        row = 0
        col = 0
        for gen_num, gen_text in generation_data:
            var = tk.BooleanVar(value=True)
            self.game.generation_vars[gen_num] = var
            
            cb = tk.Checkbutton(
                grid_frame,
                text=gen_text,
                variable=var,
                font=('Arial', 14),
                fg='#222222',
                bg='#3d7dca',
                selectcolor='#cccccc',
                activebackground='#3d7dca',
                activeforeground='#222222',
                command=self.game.on_generation_changed,
                anchor='w',  # Align text to the left
                justify='left'
            )
            cb.grid(row=row, column=col, padx=10, pady=5, sticky='w')
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Button frame
        button_frame = tk.Frame(self.container, bg='#3d7dca')
        button_frame.pack(pady=30)
        
        # Confirm button
        self.confirm_button = tk.Button(
            button_frame,
            text="Continue to Player Setup",
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
            command=self.confirm_generation_selection,
            cursor='hand2'
        )
        self.confirm_button.pack()
        
        # Store reference to button in game instance
        self.game.confirm_button = self.confirm_button
        
        # Update initial state
        self.game.update_selected_generations()
        self.game.update_confirm_button_state()
    
    def confirm_generation_selection(self):
        """Confirm generation selection and proceed to player setup"""
        if self.game.selected_generations:
            print(f"🎮 Selected generations: {sorted(self.game.selected_generations)}")
            self.game.setup_player(1)
        else:
            messagebox.showwarning("No Selection", "Please select at least one generation!")
