import sqlite3

# Connect to or create the SQLite database
conn = sqlite3.connect('farmhub.db')
c = conn.cursor()

# ✅ Create 'users' table
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

# ✅ Create 'contacts' table
c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

# 🚨 Drop existing inventory table if it exists (DELETES ALL INVENTORY DATA)
c.execute('DROP TABLE IF EXISTS inventory')

# ✅ Recreate inventory table with user_id for account-specific inventory
c.execute('''
    CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit TEXT,
        date_added TEXT DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("✅ Database initialized. Inventory table reset successfully!")
