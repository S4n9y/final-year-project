import sqlite3

# Connect to or create the SQLite database
conn = sqlite3.connect('farmhub.db')
c = conn.cursor()

# Create a 'users' table with all required fields
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        dob TEXT NOT NULL,
        gender TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
# Create a 'contacts' table for storing contact form data
c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

# Save and close the connection
conn.commit()
conn.close()

print("Database and 'users' table created successfully with all user details.")
