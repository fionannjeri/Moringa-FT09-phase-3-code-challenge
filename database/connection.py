import sqlite3

# Create a connection to the database
CONN = sqlite3.connect('magazine.db')
# Create a cursor object to execute SQL commands
CURSOR = CONN.cursor()

# Create the tables if they don't exist
def create_tables():
    # Create authors table
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    # Create magazines table
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    # Create articles table with foreign keys
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )
    """)

    # Commit the changes
    CONN.commit()

# Call create_tables when the module is imported
create_tables()

# Enable foreign key support
CURSOR.execute("PRAGMA foreign_keys = ON")

# Configure the connection to return rows as dictionaries
CONN.row_factory = sqlite3.Row