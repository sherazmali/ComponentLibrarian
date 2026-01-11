"""
Database Manager Module for Component Librarian
Handles all SQLite database operations using MVC architecture.
Follows design specification from Section 3.2.3 for database interaction.
"""

import sqlite3
from datetime import datetime

class DatabaseManager:
    """
    Manages all database operations for the Component Librarian application.
    Implements CRUD operations and follows the 'workhorse' function pattern.
    """
    
    def __init__(self, db_name="component_librarian.db"):
        """
        Initialize database connection and create tables if they don't exist.
        
        Args:
            db_name (str): Name of the SQLite database file. 
                          Defaults to 'component_librarian.db'
        """
        self.db_name = db_name
        # Create the components table on initialization
        self.create_table()
    
    def create_table(self):
        """
        Creates the components table as defined in Section 2.4 of requirements.
        
        Table structure includes:
        - component_id: Primary key with auto-increment
        - name: Component name (required)
        - pattern_name: Design pattern type
        - pattern_category: Pattern classification
        - language: Programming language
        - description: Component description
        - code_snippet: Actual code example
        - author: Creator of the component
        - date_added: Automatic timestamp
        
        Uses SQLite's 'IF NOT EXISTS' to avoid errors on re-creation.
        """
        sql = """
        CREATE TABLE IF NOT EXISTS components (
            component_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,                -- Component name (required)
            pattern_name TEXT,                 -- e.g., 'Creational', 'Structural'
            pattern_category TEXT,             -- e.g., 'Design Pattern', 'Algorithm'
            language TEXT,                     -- e.g., 'Python', 'Java'
            description TEXT,                  -- Detailed explanation
            code_snippet TEXT,                 -- Actual code example
            author TEXT,                       -- Component author
            date_added DATE                    -- Auto-added creation date
        )
        """
        # Execute the table creation query
        self.execute_query(sql, is_select=False)
    
    def execute_query(self, sql_query, params=(), is_select=False):
        """
        The 'workhorse' function described in Section 3.2.3.
        Handles all SQL operations with proper connection management and error handling.
        
        Features:
        1. Automatic connection opening/closing (context manager)
        2. Parameterized queries to prevent SQL injection
        3. Error handling with informative messages
        4. Returns dictionary results for SELECT queries
        
        Args:
            sql_query (str): SQL query to execute
            params (tuple): Query parameters for safe substitution
            is_select (bool): True for SELECT queries, False for INSERT/UPDATE/DELETE
        
        Returns:
            - For SELECT: List of dictionaries (each row as dict)
            - For other queries: Boolean success indicator
            - On error: Empty list (for SELECT) or False (for other)
        """
        try:
            # Context manager automatically handles connection open/close
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Execute with parameters (prevents SQL injection)
                cursor.execute(sql_query, params)
                
                if is_select:
                    # Get column names for dictionary conversion
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                    # Convert each row to dictionary with column names as keys
                    return [dict(zip(columns, row)) for row in results]
                else:
                    # Commit changes for INSERT/UPDATE/DELETE
                    conn.commit()
                    return True
        except sqlite3.Error as e:
            # Log database errors for debugging
            print(f"Database Error: {e}")
            # Return appropriate failure value
            return False if not is_select else []
    
    def insert_component(self, name, pattern_name, pattern_category, language, 
                        description, code_snippet, author):
        """
        Implements the CREATE operation from CRUD.
        Adds a new component record to the database.
        
        Args:
            name (str): Component name (required)
            pattern_name (str): Design pattern type
            pattern_category (str): Pattern classification
            language (str): Programming language
            description (str): Component description
            code_snippet (str): Actual code example
            author (str): Component author
        
        Returns:
            bool: True if successful, False otherwise
        """
        sql = """
        INSERT INTO components 
        (name, pattern_name, pattern_category, language, description, 
         code_snippet, author, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Get current date in YYYY-MM-DD format
        date_now = datetime.now().strftime("%Y-%m-%d")
        # Execute insert query with all parameters
        return self.execute_query(sql, 
            (name, pattern_name, pattern_category, language, 
             description, code_snippet, author, date_now), 
            is_select=False)
    
    def search_components(self, keyword="", pattern_filter="", language_filter=""):
        """
        Search components with flexible filtering options.
        Supports keyword search and specific pattern/language filters.
        
        Args:
            keyword (str): Search term for name or description (LIKE search)
            pattern_filter (str): Filter by specific pattern type (exact match)
            language_filter (str): Filter by programming language (exact match)
        
        Returns:
            list: List of component dictionaries matching criteria
        """
        # Start with base query (1=1 allows easy WHERE clause building)
        query = "SELECT * FROM components WHERE 1=1"
        parameters = []
        
        # Add keyword filter (searches both name and description)
        if keyword:
            query += " AND (name LIKE ? OR description LIKE ?)"
            # Use wildcards for partial matching
            parameters.extend([f'%{keyword}%', f'%{keyword}%'])
        
        # Add pattern type filter
        if pattern_filter:
            query += " AND pattern_name = ?"
            parameters.append(pattern_filter)
        
        # Add programming language filter
        if language_filter:
            query += " AND language = ?"
            parameters.append(language_filter)
        
        # Execute the dynamically built query
        return self.execute_query(query, parameters, is_select=True)
    
    def delete_component(self, component_id):
        """
        Implements the DELETE operation from CRUD.
        Removes a component by its unique ID.
        
        Args:
            component_id (int): The ID of the component to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        sql = "DELETE FROM components WHERE component_id = ?"
        return self.execute_query(sql, (component_id,), is_select=False)
    
    def get_all_components(self):
        """
        Retrieves all components from the database.
        Primarily used for testing and debugging.
        
        Returns:
            list: All component records as dictionaries
        """
        return self.execute_query("SELECT * FROM components", is_select=True)