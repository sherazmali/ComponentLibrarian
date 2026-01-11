"""
Component Controller Module for Component Librarian
Implements business logic layer following MVC architecture.
Handles data validation and coordinates between View and Model layers.
"""

from database import DatabaseManager

class ComponentController:
    """
    Controller layer that manages business logic and data flow.
    Acts as intermediary between GUI (View) and Database (Model).
    Implements input validation and error handling.
    """
    
    def __init__(self):
        """
        Initialize controller with a DatabaseManager instance.
        This follows MVC pattern where Controller has reference to Model.
        """
        self.db = DatabaseManager()  # Model layer instance
    
    def add_component(self, name, pattern_name, pattern_category, language, 
                     description, code_snippet, author):
        """
        Add a new component with comprehensive validation.
        Implements validation rules from Section 4.2 Interface Design Rules.
        
        Validation checks:
        1. Component name cannot be empty
        2. Code snippet cannot be empty
        3. Pattern type must be selected
        4. Programming language must be selected
        
        Args:
            name (str): Component name
            pattern_name (str): Design pattern type
            pattern_category (str): Pattern classification
            language (str): Programming language
            description (str): Component description
            code_snippet (str): Actual code example
            author (str): Component author
        
        Returns:
            tuple: (success: bool, message: str)
                   success: True if component added, False otherwise
                   message: User-friendly status message
        """
        # === VALIDATION SECTION ===
        # Check 1: Component name is required
        if not name or not name.strip():
            return False, "Component name is required."
        
        # Check 2: Code snippet is required
        if not code_snippet or not code_snippet.strip():
            return False, "Code snippet is required."
        
        # Check 3: Pattern type must be selected
        if not pattern_name:
            return False, "Pattern type is required."
        
        # Check 4: Programming language must be selected
        if not language:
            return False, "Programming language is required."
        
        # === DATABASE OPERATION ===
        # All validation passed, proceed with database insertion
        success = self.db.insert_component(
            name.strip(),           # Remove extra whitespace
            pattern_name, 
            pattern_category, 
            language, 
            description.strip(),    # Clean description
            code_snippet.strip(),   # Clean code snippet
            author.strip()          # Clean author name
        )
        
        # === RESPONSE HANDLING ===
        if success:
            return True, "Component saved successfully!"
        else:
            return False, "Database error occurred."
    
    def search_components(self, keyword="", pattern_filter="", language_filter=""):
        """
        Search for components using multiple filter criteria.
        Delegates search logic to DatabaseManager.
        
        Args:
            keyword (str): Search term for name/description
            pattern_filter (str): Filter by pattern type
            language_filter (str): Filter by programming language
        
        Returns:
            list: Component dictionaries matching search criteria
        """
        # Delegate search to Model layer (DatabaseManager)
        return self.db.search_components(keyword, pattern_filter, language_filter)
    
    def delete_component(self, component_id):
        """
        Delete a component by its unique ID.
        Provides user-friendly error messages.
        
        Args:
            component_id (int/str): ID of component to delete
        
        Returns:
            tuple: (success: bool, message: str)
        """
        # Convert to int if string provided
        if isinstance(component_id, str):
            try:
                component_id = int(component_id)
            except ValueError:
                return False, "Invalid component ID."
        
        # Attempt deletion
        success = self.db.delete_component(component_id)
        
        if success:
            return True, "Component deleted successfully!"
        else:
            return False, "Error deleting component."
    
    def get_all_components(self):
        """
        Get all components (primarily for testing purposes).
        
        Returns:
            list: All components in the database
        """
        return self.db.get_all_components()