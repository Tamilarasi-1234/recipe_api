import sqlite3

# Connect to the SQLite database (it will create if not exists)
conn = sqlite3.connect("recipes.db")
cur = conn.cursor()

# Create recipes table
cur.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cuisine VARCHAR(255),
    title VARCHAR(255),
    rating FLOAT,
    prep_time INT,
    cook_time INT,
    total_time INT,
    description TEXT,
    nutrients TEXT,
    serves VARCHAR(50)
)
""")

print("Database and table created successfully.")

conn.commit()
conn.close()
