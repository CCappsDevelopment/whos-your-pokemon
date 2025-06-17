"""
Autocomplete Entry widget for Pokemon Guess Game
"""
import tkinter as tk
from tkinter import ttk


class AutocompleteEntry(tk.Frame):
    """
    Autocomplete text entry widget with fuzzy search functionality and Pokemon sprite support
    """
    def __init__(self, parent, values, image_loader=None, data_manager=None, **kwargs):
        super().__init__(parent)
        
        self.values = values
        self.image_loader = image_loader
        self.data_manager = data_manager
        self.var = tk.StringVar()
        self.var.trace('w', self.on_text_changed)
        
        # Entry widget with better visual feedback
        self.entry = tk.Entry(
            self,
            textvariable=self.var,
            font=('Arial', 14),
            bg='#cccccc',
            fg='#222222',
            insertbackground='blue',  # Cursor color - more visible
            insertwidth=3,  # Wider cursor
            relief='solid',
            borderwidth=2,
            highlightbackground='#003a70',
            highlightcolor='#003a70',
            highlightthickness=2,
            **kwargs
        )
        self.entry.pack(fill='x')
        
        # Frame for suggestions (initially hidden)
        self.suggestions_frame = tk.Frame(
            self,
            relief='solid',
            borderwidth=1,
            bg='#cccccc'
        )
        
        # Scrollable area for suggestions
        self.canvas = tk.Canvas(
            self.suggestions_frame,
            bg='#cccccc',
            highlightthickness=0,
            height=300  # Max height for 3-4 Pokemon entries
        )
        self.scrollbar = ttk.Scrollbar(
            self.suggestions_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg='#cccccc')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window and configure it to fill canvas width
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind canvas resize to update scrollable frame width
        def configure_scrollable_frame(event):
            # Update the scrollable frame to match canvas width
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.canvas.bind('<Configure>', configure_scrollable_frame)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Store suggestion items for interaction
        self.suggestion_items = []
        
        # Bind events
        self.entry.bind('<Down>', self.on_down_arrow)
        self.entry.bind('<Up>', self.on_up_arrow)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Tab>', self.on_tab)
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<KeyPress>', self.on_key_press)  # Track typing
        
        # Mouse wheel scrolling for canvas
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
        self.suggestions_visible = False
        self.selecting_from_list = False
        self.selection_made = False  # Track if user made a selection
        self.selected_index = -1  # Track selected suggestion
    
    def fuzzy_search(self, query, items):
        """
        Perform fuzzy search on items based on query
        Returns list of items that match the query
        """
        if not query:
            return []
        
        query = query.lower()
        matches = []
        
        for item in items:
            item_lower = item.lower()
            
            # Exact match gets highest priority
            if item_lower == query:
                matches.insert(0, item)
            # Starts with query gets second priority
            elif item_lower.startswith(query):
                matches.append(item)
            # Contains query gets third priority
            elif query in item_lower:
                matches.append(item)
            # Fuzzy match - all characters of query appear in order
            else:
                query_index = 0
                for char in item_lower:
                    if query_index < len(query) and char == query[query_index]:
                        query_index += 1
                
                if query_index == len(query):
                    matches.append(item)
        
        return matches[:8]  # Limit to 8 suggestions for better UI
        
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def create_pokemon_suggestion_item(self, parent, pokemon_name, index):
        """Create a single Pokemon suggestion item with sprite"""
        # Main container frame - fill entire width
        item_frame = tk.Frame(
            parent,
            bg='#cccccc',
            relief='flat',
            borderwidth=0,
            cursor='hand2'
        )
        item_frame.pack(fill='both', expand=True, padx=0, pady=1)
        
        # Configure grid weights to fill width properly
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=0)
        
        # Pokemon name label (left side) - expand to fill available space
        name_label = tk.Label(
            item_frame,
            text=pokemon_name,
            font=('Arial', 12),
            fg='#222222',
            bg='#cccccc',
            anchor='w',
            padx=10,
            pady=5
        )
        name_label.grid(row=0, column=0, sticky='ew')
        
        # Pokemon sprite container (right side) - fixed size at the right edge
        sprite_container = tk.Frame(
            item_frame,
            bg='#999999',  # Grey background
            relief='solid',
            borderwidth=1,  # Black border
            width=68,  # 64px + 2px padding on each side
            height=68
        )
        sprite_container.grid(row=0, column=1, padx=(5, 5), pady=2, sticky='e')
        sprite_container.grid_propagate(False)
        
        # Pokemon sprite label
        sprite_label = tk.Label(
            sprite_container,
            bg='#999999',
            borderwidth=0,
            highlightthickness=0
        )
        sprite_label.pack(expand=True)
        
        # Load Pokemon sprite if available
        if self.image_loader and self.data_manager:
            sprite_url = self.data_manager.get_pokemon_sprite_url(pokemon_name)
            if sprite_url:
                image = self.image_loader.load_pokemon_image_autocomplete(pokemon_name, sprite_url)
                if image:
                    sprite_label.configure(image=image)
                    sprite_label.image = image  # Keep reference
        
        # Bind click events to all components
        def on_click(event):
            self.select_item_by_index(index)
        
        def on_enter(event):
            self.highlight_item(index)
        
        def on_leave(event):
            self.unhighlight_item(index)
        
        # Bind events to all widgets in the item
        for widget in [item_frame, name_label, sprite_container, sprite_label]:
            widget.bind('<Button-1>', on_click)
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
        
        return {
            'frame': item_frame,
            'name_label': name_label,
            'sprite_container': sprite_container,
            'sprite_label': sprite_label,
            'pokemon_name': pokemon_name
        }
    
    def highlight_item(self, index):
        """Highlight a suggestion item"""
        if 0 <= index < len(self.suggestion_items):
            self.selected_index = index
            item = self.suggestion_items[index]
            # Change background to selection color
            item['frame'].configure(bg='#3d7dca')
            item['name_label'].configure(bg='#3d7dca', fg='white')
            
            # Unhighlight all other items
            for i, other_item in enumerate(self.suggestion_items):
                if i != index:
                    other_item['frame'].configure(bg='#cccccc')
                    other_item['name_label'].configure(bg='#cccccc', fg='#222222')
    
    def unhighlight_item(self, index):
        """Remove highlight from a suggestion item"""
        if 0 <= index < len(self.suggestion_items):
            item = self.suggestion_items[index]
            if self.selected_index != index:
                item['frame'].configure(bg='#cccccc')
                item['name_label'].configure(bg='#cccccc', fg='#222222')
    
    def select_item_by_index(self, index):
        """Select an item by its index"""
        if 0 <= index < len(self.suggestion_items):
            pokemon_name = self.suggestion_items[index]['pokemon_name']
            self.selecting_from_list = True
            self.var.set(pokemon_name)
            self.selecting_from_list = False
            self.selection_made = True
            self.hide_suggestions()
            self.entry.focus_set()
            self.entry.icursor(tk.END)
    
    def on_text_changed(self, *args):
        """Handle text changes in the entry widget"""
        if self.selecting_from_list:
            return
        
        # Don't show suggestions if user made a selection and hasn't typed since
        if self.selection_made:
            return
            
        query = self.var.get()
        matches = self.fuzzy_search(query, self.values)
        
        if matches and len(query) > 0:
            self.show_suggestions(matches)
        else:
            self.hide_suggestions()
    
    def on_key_press(self, event):
        """Handle key press events to detect typing"""
        # User is typing, reset selection flag
        self.selection_made = False
    
    def show_suggestions(self, matches):
        """Show the suggestions with Pokemon sprites"""
        # Clear existing suggestions
        for child in self.scrollable_frame.winfo_children():
            child.destroy()
        self.suggestion_items.clear()
        
        # Create new suggestion items
        for i, pokemon_name in enumerate(matches):
            item = self.create_pokemon_suggestion_item(self.scrollable_frame, pokemon_name, i)
            self.suggestion_items.append(item)
        
        # Show suggestions frame
        if not self.suggestions_visible:
            self.suggestions_frame.pack(fill='x', pady=(2, 0))
            self.suggestions_visible = True
            
        # Reset scroll to top
        self.canvas.yview_moveto(0)
        self.selected_index = -1
    
    def hide_suggestions(self):
        """Hide the suggestions frame"""
        if self.suggestions_visible:
            self.suggestions_frame.pack_forget()
            self.suggestions_visible = False
            self.selected_index = -1
    
    def on_focus_in(self, event):
        """Handle entry gaining focus"""
        self.entry.configure(relief='solid', borderwidth=3, highlightbackground='#003a70', bg='#cccccc')
        # Show suggestions if there's text
        if self.var.get():
            self.on_text_changed()
    
    def on_focus_out(self, event):
        """Handle entry losing focus"""
        self.entry.configure(relief='solid', borderwidth=1, highlightbackground='#003a70', bg='#cccccc')
        # Delay hiding to allow for mouse clicks on suggestions
        self.after(200, self.check_and_hide_suggestions)
    
    def check_and_hide_suggestions(self):
        """Check if focus is still in widget before hiding"""
        try:
            focused = self.focus_get()
            # Check if focus is on entry or any suggestion item
            if focused != self.entry and not self.is_focus_in_suggestions(focused):
                self.hide_suggestions()
        except:
            self.hide_suggestions()
    
    def is_focus_in_suggestions(self, widget):
        """Check if the focused widget is within the suggestions frame"""
        if not widget:
            return False
        parent = widget
        while parent:
            if parent == self.suggestions_frame:
                return True
            try:
                parent = parent.master
            except:
                break
        return False
    
    def on_down_arrow(self, event):
        """Handle down arrow key - navigate suggestions"""
        if self.suggestions_visible and len(self.suggestion_items) > 0:
            next_index = 0 if self.selected_index == -1 else min(self.selected_index + 1, len(self.suggestion_items) - 1)
            self.highlight_item(next_index)
            return 'break'
    
    def on_up_arrow(self, event):
        """Handle up arrow key - navigate suggestions"""
        if self.suggestions_visible and len(self.suggestion_items) > 0:
            prev_index = len(self.suggestion_items) - 1 if self.selected_index == -1 else max(self.selected_index - 1, 0)
            self.highlight_item(prev_index)
            return 'break'
    
    def on_enter(self, event):
        """Handle enter key - select current item"""
        if self.suggestions_visible:
            if self.selected_index >= 0:
                self.select_item_by_index(self.selected_index)
                return 'break'
            elif len(self.suggestion_items) > 0:
                # Select first item if nothing is selected
                self.select_item_by_index(0)
                return 'break'
    
    def on_tab(self, event):
        """Handle tab key - select first suggestion"""
        if self.suggestions_visible and len(self.suggestion_items) > 0:
            self.select_item_by_index(0)
            return 'break'
    
    def get(self):
        """Get the current value"""
        return self.var.get()
    
    def set(self, value):
        """Set the current value"""
        self.var.set(value)
