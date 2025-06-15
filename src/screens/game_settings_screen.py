"""
Game settings screen for Pokemon Guess Game
"""
import tkinter as tk
from tkinter import messagebox, ttk
from .base_screen import BaseScreen


class GameSettingsScreen(BaseScreen):
    """Screen for configuring game settings including generations, variants, and pokemon selection"""
    
    def show(self):
        """Display the game settings screen"""
        self.clear_screen()
        
        # Main container - no scrollbar needed with horizontal layout
        self.container = tk.Frame(self.root, bg='#3d7dca')
        self.container.pack(expand=True, fill='both', padx=30, pady=20)
        
        # Logo
        logo_image = self.game.image_loader.load_logo_image('game-settings-logo.png', max_width=500, max_height=80)
        if logo_image:
            logo_label = tk.Label(
                self.container,
                image=logo_image,
                bg='#3d7dca'
            )
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(pady=(10, 15))
        else:
            # Fallback to text if logo doesn't load
            title_label = tk.Label(
                self.container,
                text="Game Settings",
                font=('Arial', 32, 'bold'),
                fg='#003a70',
                bg='#3d7dca'
            )
            title_label.pack(pady=(10, 15))
        
        # Create a centered content frame to cluster all sections together
        content_frame = tk.Frame(self.container, bg='#3d7dca')
        content_frame.pack(expand=True)
        
        # Create horizontal layout frame for generations and variants
        horizontal_frame = tk.Frame(content_frame, bg='#3d7dca')
        horizontal_frame.pack(pady=(0, 5))
        
        # Configure columns to be equal width with a small gap for the divider
        horizontal_frame.grid_columnconfigure(0, weight=1)
        horizontal_frame.grid_columnconfigure(1, weight=0)  # divider column
        horizontal_frame.grid_columnconfigure(2, weight=1)
        
        # Create left column for generations
        left_column = tk.Frame(horizontal_frame, bg='#3d7dca')
        left_column.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Create vertical divider - same height as the variant section
        vertical_divider = tk.Frame(horizontal_frame, bg='#222222', width=1)
        vertical_divider.grid(row=0, column=1, sticky='ns')
        
        # Create right column for variants  
        right_column = tk.Frame(horizontal_frame, bg='#3d7dca')
        right_column.grid(row=0, column=2, sticky='nsew', padx=(15, 0))
        
        # Create sections in their respective columns
        self.create_generation_section(left_column)
        self.create_variants_section(right_column)
        
        # Add horizontal divider between top sections and pokemon selection
        horizontal_divider_frame = tk.Frame(content_frame, bg='#3d7dca')
        horizontal_divider_frame.pack(fill='x', pady=(10, 10))
        
        # Create the horizontal divider at 66% width, centered
        horizontal_divider = tk.Frame(horizontal_divider_frame, bg='#222222', height=1)
        horizontal_divider.pack(fill='x', padx=(100, 100))
        
        # Create pokemon selection section below the divider
        self.create_pokemon_selection_section(content_frame)
        
        # Confirm button - closer to the selection section
        self.confirm_button = tk.Button(
            content_frame,
            text="Continue to Player Setup",
            font=('Arial', 16, 'bold'),
            bg='#ffcb05',
            fg='#222222',
            highlightbackground='#222222',
            highlightcolor='#222222',
            highlightthickness=2,
            relief='solid',
            borderwidth=2,
            padx=30,
            pady=12,
            command=self.confirm_settings,
            cursor='hand2'
        )
        self.confirm_button.pack(pady=8)
        
        # Store reference to button in game instance
        self.game.confirm_button = self.confirm_button
        
        # Initialize states
        self.game.update_selected_generations()
        self.game.update_selected_variants()
        self.game.update_confirm_button_state()
    
    def create_generation_section(self, parent_frame):
        """Create the generation selection section"""
        # Section header
        gen_header = tk.Label(
            parent_frame,
            text="Generation Selection",
            font=('Arial', 24, 'bold'),
            fg='#003a70',
            bg='#3d7dca'
        )
        gen_header.pack(pady=(0, 8))
        
        # Generation selection frame - no border
        generation_frame = tk.Frame(parent_frame, bg='#3d7dca')
        generation_frame.pack(pady=5, fill='x')
        
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
        all_regions_frame = tk.Frame(generation_frame, bg='#3d7dca')
        all_regions_frame.pack(pady=(8, 8))
        
        self.game.all_regions_var = tk.BooleanVar(value=True)
        all_regions_cb = tk.Checkbutton(
            all_regions_frame,
            text="All Generations",
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
        grid_frame = tk.Frame(generation_frame, bg='#3d7dca')
        grid_frame.pack(pady=(8, 12))
        
        # Configure grid columns for consistent alignment
        for col in range(3):
            grid_frame.grid_columnconfigure(col, weight=1, uniform="gen_col")
        
        # Initialize generation variables in game instance
        if not hasattr(self.game, 'generation_vars'):
            self.game.generation_vars = {}
        
        row = 0
        col = 0
        for gen_num, gen_text in generation_data:
            var = tk.BooleanVar(value=True)
            self.game.generation_vars[gen_num] = var
            
            cb = tk.Checkbutton(
                grid_frame,
                text=gen_text,
                variable=var,
                font=('Arial', 16),
                fg='#222222',
                bg='#3d7dca',
                selectcolor='#cccccc',
                activebackground='#3d7dca',
                activeforeground='#222222',
                command=self.game.on_generation_changed,
                anchor='w',
                justify='left'
            )
            cb.grid(row=row, column=col, padx=8, pady=3, sticky='w')
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def create_variants_section(self, parent_frame):
        """Create the variants selection section"""
        # Section header
        variant_header = tk.Label(
            parent_frame,
            text="Variant Selection",
            font=('Arial', 24, 'bold'),
            fg='#003a70',
            bg='#3d7dca'
        )
        variant_header.pack(pady=(0, 8))
        
        # Variants selection frame - no border
        variants_frame = tk.Frame(parent_frame, bg='#3d7dca')
        variants_frame.pack(pady=5, fill='x')
        
        # Initialize variant variables in game instance
        if not hasattr(self.game, 'variant_vars'):
            self.game.variant_vars = {}
        
        # Variant data
        variant_data = [
            'Regional - Alolan',
            'Regional - Galarian', 
            'Regional - Hisuian',
            'Regional - Paldean',
            'Gigantamax',
            'Mega',
            'Special Pikachus',
            'Totem Pokemon',
            'Paradox Pokemon',
            'Form Variants',
            'Size Variants'
        ]
        
        # All Variants checkbox (first row)
        all_variants_frame = tk.Frame(variants_frame, bg='#3d7dca')
        all_variants_frame.pack(pady=(8, 8))
        
        self.game.all_variants_var = tk.BooleanVar(value=True)
        all_variants_cb = tk.Checkbutton(
            all_variants_frame,
            text="All Variants",
            variable=self.game.all_variants_var,
            font=('Arial', 16, 'bold'),
            fg='#003a70',
            bg='#3d7dca',
            selectcolor='#cccccc',
            activebackground='#3d7dca',
            activeforeground='#003a70',
            command=self.game.on_all_variants_changed
        )
        all_variants_cb.pack()
        
        # Individual variant checkboxes (in 3 columns)
        variant_grid_frame = tk.Frame(variants_frame, bg='#3d7dca')
        variant_grid_frame.pack(pady=(8, 12))
        
        # Configure grid columns for consistent alignment
        for col in range(3):
            variant_grid_frame.grid_columnconfigure(col, weight=1, uniform="variant_col")
        
        row = 0
        col = 0
        for variant_name in variant_data:
            var = tk.BooleanVar(value=True)
            self.game.variant_vars[variant_name] = var
            
            cb = tk.Checkbutton(
                variant_grid_frame,
                text=variant_name,
                variable=var,
                font=('Arial', 16),
                fg='#222222',
                bg='#3d7dca',
                selectcolor='#cccccc',
                activebackground='#3d7dca',
                activeforeground='#222222',
                command=self.game.on_variant_changed,
                anchor='w',
                justify='left'
            )
            cb.grid(row=row, column=col, padx=8, pady=3, sticky='w')
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def create_pokemon_selection_section(self, parent_frame):
        """Create the Pokemon selection method section"""
        # Section header
        selection_header = tk.Label(
            parent_frame,
            text="Pokemon Selection Method",
            font=('Arial', 24, 'bold'),
            fg='#003a70',
            bg='#3d7dca'
        )
        selection_header.pack(pady=(15, 8))
        
        # Pokemon selection frame - centered, no border
        selection_frame = tk.Frame(parent_frame, bg='#3d7dca')
        selection_frame.pack(pady=5, padx=100, fill='x')
        
        # Description
        desc_label = tk.Label(
            selection_frame,
            text="Choose how the 24 Pokemon for each player are selected:",
            font=('Arial', 16),
            fg='#222222',
            bg='#3d7dca'
        )
        desc_label.pack(pady=(8, 8))
        
        # Dropdown frame
        dropdown_frame = tk.Frame(selection_frame, bg='#3d7dca')
        dropdown_frame.pack(pady=(5, 12))
        
        # Selection method dropdown
        self.game.pokemon_selection_var = tk.StringVar(value="randomize")
        selection_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.game.pokemon_selection_var,
            values=["randomize", "manual"],
            state="readonly",
            font=('Arial', 16),
            width=15
        )
        selection_dropdown.pack()
        selection_dropdown.bind('<<ComboboxSelected>>', self.game.on_pokemon_selection_changed)
    
    
    def confirm_settings(self):
        """Confirm game settings and proceed to player setup"""
        if self.game.selected_generations:
            print(f"🎮 Selected generations: {sorted(self.game.selected_generations)}")
            print(f"🔮 Selected variants: {sorted(self.game.selected_variants) if hasattr(self.game, 'selected_variants') else 'All'}")
            print(f"🎯 Pokemon selection method: {self.game.pokemon_selection_var.get()}")
            self.game.setup_player(1)
        else:
            messagebox.showwarning("No Selection", "Please select at least one generation!")
