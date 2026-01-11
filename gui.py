"""
GUI Module for Component Librarian
Tkinter-based user interface following MVC architecture.
Implements the View layer with responsive design and user-friendly interactions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from controller import ComponentController

class ComponentLibrarianGUI:
    """
    Main GUI class that implements the View layer of MVC.
    Provides user interface for component management with:
    - Component listing and search
    - Add/edit/delete operations
    - Detailed component viewing
    - Responsive filtering
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root (tk.Tk): The main Tkinter root window
        """
        self.root = root
        # Set window properties
        self.root.title("Component Librarian - MVC Version")
        self.root.geometry("900x700")  # Width x Height
        
        # Initialize Controller (which initializes Model)
        self.controller = ComponentController()
        
        # Store currently selected component ID for operations
        self.selected_component_id = None
        
        # Build the interface
        self.create_main_interface()
        
        # Load initial component list
        self.refresh_component_list()
    
    def create_main_interface(self):
        """
        Creates the main application window with all UI components.
        Organized into sections: Search, Filters, Results, Details.
        """
        # === MAIN CONTAINER ===
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure responsive grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)  # Search field expands
        main_frame.rowconfigure(2, weight=1)     # Treeview expands
        
        # === SEARCH SECTION ===
        ttk.Label(main_frame, text="Search Components:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Search entry with real-time filtering
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(main_frame, textvariable=self.search_var, width=50)
        self.search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search_change)  # Real-time search
        
        # === FILTERS SECTION ===
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Pattern filter dropdown
        ttk.Label(filter_frame, text="Pattern:").grid(row=0, column=0, padx=(0, 5))
        self.pattern_var = tk.StringVar()
        self.pattern_combo = ttk.Combobox(filter_frame, textvariable=self.pattern_var, width=15)
        self.pattern_combo['values'] = ['', 'Structural', 'Behavioral', 'Creational']
        self.pattern_combo.grid(row=0, column=1, padx=(0, 15))
        self.pattern_combo.bind('<<ComboboxSelected>>', self.on_search_change)
        
        # Language filter dropdown
        ttk.Label(filter_frame, text="Language:").grid(row=0, column=2, padx=(0, 5))
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(filter_frame, textvariable=self.language_var, width=15)
        self.language_combo['values'] = ['', 'C', 'C++', 'Python', 'Java', 'JavaScript']
        self.language_combo.grid(row=0, column=3, padx=(0, 15))
        self.language_combo.bind('<<ComboboxSelected>>', self.on_search_change)
        
        # Add Component button
        ttk.Button(filter_frame, text="Add Component", 
                  command=self.open_add_dialog).grid(row=0, column=4, padx=(20, 0))
        
        # === RESULTS SECTION ===
        ttk.Label(main_frame, text="Components:").grid(
            row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        # Treeview for displaying component list
        columns = ('Name', 'Pattern', 'Language', 'Description')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # Define column headings
        self.tree.heading('Name', text='Name')
        self.tree.heading('Pattern', text='Pattern')
        self.tree.heading('Language', text='Language')
        self.tree.heading('Description', text='Description')
        
        # Define column widths
        self.tree.column('Name', width=150)
        self.tree.column('Pattern', width=100)
        self.tree.column('Language', width=80)
        self.tree.column('Description', width=300)
        
        self.tree.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event to show details
        self.tree.bind('<<TreeviewSelect>>', self.on_component_select)
        
        # === DETAILS SECTION ===
        details_frame = ttk.LabelFrame(main_frame, text="Component Details", padding="5")
        details_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        details_frame.columnconfigure(1, weight=1)
        
        # Component name display
        ttk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.detail_name = ttk.Label(details_frame, text="")
        self.detail_name.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Pattern type display
        ttk.Label(details_frame, text="Pattern:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.detail_pattern = ttk.Label(details_frame, text="")
        self.detail_pattern.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Language display
        ttk.Label(details_frame, text="Language:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.detail_language = ttk.Label(details_frame, text="")
        self.detail_language.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Description display
        ttk.Label(details_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.detail_description = ttk.Label(details_frame, text="")
        self.detail_description.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Author and date display
        ttk.Label(details_frame, text="Author:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.detail_author = ttk.Label(details_frame, text="")
        self.detail_author.grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # Code snippet display (scrollable text area)
        ttk.Label(details_frame, text="Code:").grid(row=5, column=0, sticky=tk.NW, pady=2)
        self.code_text = scrolledtext.ScrolledText(details_frame, width=70, height=10)
        self.code_text.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Delete button (only enabled when component selected)
        ttk.Button(details_frame, text="Delete Component", 
                  command=self.delete_selected_component).grid(
                      row=6, column=0, columnspan=2, pady=(10, 0))
    
    def on_search_change(self, event=None):
        """
        Called when search criteria change (typing or filter selection).
        Triggers refresh of component list.
        
        Args:
            event: Tkinter event object (optional)
        """
        self.refresh_component_list()
    
    def refresh_component_list(self):
        """
        Refreshes the component list based on current search/filter criteria.
        Queries controller and updates treeview display.
        """
        # Clear existing items from treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get current search parameters
        keyword = self.search_var.get()
        pattern_filter = self.pattern_var.get()
        language_filter = self.language_var.get()
        
        # Search components through Controller
        components = self.controller.search_components(keyword, pattern_filter, language_filter)
        
        # Add components to treeview
        for comp in components:
            # Truncate long descriptions for display
            description = comp['description']
            if len(description) > 50:
                description = description[:50] + "..."
            
            # Insert component into treeview
            self.tree.insert('', 'end', values=(
                comp['name'],
                comp['pattern_name'],
                comp['language'],
                description
            ), tags=(comp['component_id'],))  # Store ID in tags for retrieval
    
    def on_component_select(self, event):
        """
        Called when user selects a component in the list.
        Loads and displays full component details.
        
        Args:
            event: Tkinter selection event
        """
        selection = self.tree.selection()
        if selection:
            # Get selected item and its stored component ID
            item = selection[0]
            self.selected_component_id = self.tree.item(item, 'tags')[0]
            
            # Get all components and find the selected one
            components = self.controller.search_components()
            component = next((comp for comp in components 
                            if comp['component_id'] == int(self.selected_component_id)), None)
            
            if component:
                # Update detail labels with component information
                self.detail_name.config(text=component['name'])
                self.detail_pattern.config(text=component['pattern_name'])
                self.detail_language.config(text=component['language'])
                self.detail_description.config(text=component['description'])
                self.detail_author.config(text=f"{component['author']} - {component['date_added']}")
                
                # Display code snippet in scrollable text area
                self.code_text.delete(1.0, tk.END)  # Clear existing
                self.code_text.insert(1.0, component['code_snippet'])
    
    def delete_selected_component(self):
        """
        Deletes the currently selected component after confirmation.
        Shows success/error messages and refreshes the list.
        """
        # Check if a component is selected
        if not self.selected_component_id:
            messagebox.showwarning("Warning", "Please select a component to delete")
            return
        
        # Confirm deletion with user
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this component?"):
            # Delete through Controller
            success, message = self.controller.delete_component(self.selected_component_id)
            
            if success:
                messagebox.showinfo("Success", message)
                # Refresh list and clear details
                self.refresh_component_list()
                self.clear_details()
            else:
                messagebox.showerror("Error", message)
    
    def clear_details(self):
        """
        Clears the details section when no component is selected.
        Resets all detail labels and text areas.
        """
        self.selected_component_id = None
        self.detail_name.config(text="")
        self.detail_pattern.config(text="")
        self.detail_language.config(text="")
        self.detail_description.config(text="")
        self.detail_author.config(text="")
        self.code_text.delete(1.0, tk.END)
    
    def open_add_dialog(self):
        """
        Opens the 'Add New Component' dialog window.
        Creates a modal dialog for component entry.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Component")
        dialog.geometry("600x500")
        dialog.transient(self.root)  # Set as child of main window
        dialog.grab_set()  # Make dialog modal
        
        # Create add form inside dialog
        self.create_add_form(dialog)
    
    def create_add_form(self, dialog):
        """
        Creates the form for adding new components.
        
        Args:
            dialog (tk.Toplevel): The dialog window to populate
        """
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure responsive grid
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # === FORM FIELDS ===
        
        # Name field (required)
        ttk.Label(main_frame, text="Name:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, width=50)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Pattern field (required)
        ttk.Label(main_frame, text="Pattern:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        pattern_var = tk.StringVar()
        pattern_combo = ttk.Combobox(main_frame, textvariable=pattern_var, width=47)
        pattern_combo['values'] = ['Structural', 'Behavioral', 'Creational']
        pattern_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Pattern category field (optional)
        ttk.Label(main_frame, text="Pattern Category:").grid(row=2, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(main_frame, textvariable=category_var, width=47)
        category_combo['values'] = ['Container', 'Algorithm', 'Utility', 'Security', 'Other']
        category_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Language field (required)
        ttk.Label(main_frame, text="Language:*").grid(row=3, column=0, sticky=tk.W, pady=5)
        language_var = tk.StringVar()
        language_combo = ttk.Combobox(main_frame, textvariable=language_var, width=47)
        language_combo['values'] = ['C', 'C++', 'Python', 'Java', 'JavaScript']
        language_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Description field (multi-line, optional)
        ttk.Label(main_frame, text="Description:").grid(row=4, column=0, sticky=tk.W, pady=5)
        desc_entry = tk.Text(main_frame, width=50, height=3)
        desc_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Code snippet field (multi-line, required)
        ttk.Label(main_frame, text="Code Snippet:*").grid(row=5, column=0, sticky=tk.W, pady=5)
        code_entry = scrolledtext.ScrolledText(main_frame, width=50, height=10)
        code_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Author field (optional)
        ttk.Label(main_frame, text="Author:").grid(row=6, column=0, sticky=tk.W, pady=5)
        author_entry = ttk.Entry(main_frame, width=50)
        author_entry.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # === ACTION BUTTONS ===
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        def save_component():
            """
            Save button handler - validates and saves new component.
            """
            # Get all field values
            name = name_entry.get().strip()
            pattern = pattern_var.get().strip()
            category = category_var.get().strip()
            language = language_var.get().strip()
            description = desc_entry.get(1.0, tk.END).strip()
            code = code_entry.get(1.0, tk.END).strip()
            author = author_entry.get().strip()
            
            # Save through Controller (handles validation)
            success, message = self.controller.add_component(
                name, pattern, category, language, description, code, author
            )
            
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()  # Close dialog
                self.refresh_component_list()  # Refresh main list
            else:
                messagebox.showerror("Error", message)
        
        # Save and Cancel buttons
        ttk.Button(button_frame, text="Save Component", 
                  command=save_component).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", 
                  command=dialog.destroy).pack(side=tk.LEFT)


# === APPLICATION ENTRY POINT ===
if __name__ == "__main__":
    """
    Main entry point for standalone GUI execution.
    Creates Tkinter root window and starts the application.
    """
    root = tk.Tk()
    app = ComponentLibrarianGUI(root)
    root.mainloop()  # Start Tkinter event loop