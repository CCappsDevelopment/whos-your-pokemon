"""
Autocomplete Entry widget for Pokemon Guess Game
"""
import tkinter as tk


class AutocompleteEntry(tk.Frame):
    """
    Autocomplete text entry widget with fuzzy search functionality
    """
    def __init__(self, parent, values, **kwargs):
        super().__init__(parent)
        
        self.values = values
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
        
        # Listbox for suggestions (initially hidden)
        self.listbox = tk.Listbox(
            self,
            height=8,
            font=('Arial', 12),
            bg='#cccccc',
            fg='#222222',
            selectbackground='#3d7dca',
            selectforeground='white',
            relief='solid',
            borderwidth=1
        )
        
        # Bind events
        self.entry.bind('<Down>', self.on_down_arrow)
        self.entry.bind('<Up>', self.on_up_arrow)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Tab>', self.on_tab)
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<KeyPress>', self.on_key_press)  # Track typing
        
        self.listbox.bind('<Button-1>', self.on_select)
        self.listbox.bind('<ButtonRelease-1>', self.on_select)  # Also handle release
        self.listbox.bind('<Double-Button-1>', self.on_double_click)
        self.listbox.bind('<Return>', self.on_enter)
        self.listbox.bind('<FocusOut>', self.on_listbox_focus_out)
        
        self.suggestions_visible = False
        self.selecting_from_list = False
        self.selection_made = False  # Track if user made a selection
    
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
        
        return matches[:20]  # Limit to 20 suggestions
    
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
        """Show the suggestions listbox with matching items"""
        self.listbox.delete(0, tk.END)
        for match in matches:
            self.listbox.insert(tk.END, match)
        
        if not self.suggestions_visible:
            self.listbox.pack(fill='x', pady=(2, 0))
            self.suggestions_visible = True
    
    def hide_suggestions(self):
        """Hide the suggestions listbox"""
        if self.suggestions_visible:
            self.listbox.pack_forget()
            self.suggestions_visible = False
    
    def on_focus_in(self, event):
        """Handle entry gaining focus"""
        self.entry.configure(relief='solid', borderwidth=3, highlightbackground='#003a70', bg='#cccccc')
        # Show suggestions if there's text
        if self.var.get():
            self.on_text_changed()
    
    def on_focus_out(self, event):
        """Handle entry losing focus"""
        self.entry.configure(relief='solid', borderwidth=1, highlightbackground='#003a70', bg='#cccccc')
        # Delay hiding to allow for mouse clicks on listbox
        self.after(200, self.check_and_hide_suggestions)
    
    def on_listbox_focus_out(self, event):
        """Handle listbox losing focus"""
        self.after(200, self.check_and_hide_suggestions)
    
    def check_and_hide_suggestions(self):
        """Check if focus is still in widget before hiding"""
        try:
            focused = self.focus_get()
            if focused != self.entry and focused != self.listbox:
                self.hide_suggestions()
        except:
            self.hide_suggestions()
    
    def on_down_arrow(self, event):
        """Handle down arrow key - move to listbox"""
        if self.suggestions_visible and self.listbox.size() > 0:
            self.listbox.focus_set()
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return 'break'
    
    def on_up_arrow(self, event):
        """Handle up arrow key"""
        if self.suggestions_visible and self.listbox.size() > 0:
            self.listbox.focus_set()
            last_index = self.listbox.size() - 1
            self.listbox.selection_set(last_index)
            self.listbox.activate(last_index)
            return 'break'
    
    def on_enter(self, event):
        """Handle enter key - select current item"""
        if self.suggestions_visible:
            selection = self.listbox.curselection()
            if selection:
                self.select_item(selection[0])
                return 'break'
            elif self.listbox.size() > 0:
                # Select first item if nothing is selected
                self.select_item(0)
                return 'break'
    
    def on_tab(self, event):
        """Handle tab key - select first suggestion"""
        if self.suggestions_visible and self.listbox.size() > 0:
            self.select_item(0)
            return 'break'
    
    def on_select(self, event):
        """Handle mouse selection from listbox"""
        selection = self.listbox.curselection()
        if selection:
            self.select_item(selection[0])
            return 'break'
    
    def on_double_click(self, event):
        """Handle double-click selection from listbox"""
        selection = self.listbox.curselection()
        if selection:
            self.select_item(selection[0])
            return 'break'
    
    def select_item(self, index):
        """Select an item from the listbox"""
        if 0 <= index < self.listbox.size():
            selected_item = self.listbox.get(index)
            self.selecting_from_list = True
            self.var.set(selected_item)
            self.selecting_from_list = False
            self.selection_made = True  # Mark that selection was made
            self.hide_suggestions()
            self.entry.focus_set()
            # Move cursor to end
            self.entry.icursor(tk.END)
    
    def get(self):
        """Get the current value"""
        return self.var.get()
    
    def set(self, value):
        """Set the current value"""
        self.var.set(value)
