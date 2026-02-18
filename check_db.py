import sqlite3
import json

conn = sqlite3.connect("recipes.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Count recipes
cur.execute("SELECT COUNT(*) FROM recipes")
total = cur.fetchone()[0]
print(f"Total recipes: {total}\n")

# Show first 5 recipes
cur.execute("SELECT * FROM recipes LIMIT 5")
rows = cur.fetchall()

for row in rows:
    print(f"ID: {row['id']}, Title: {row['title']}, Cuisine: {row['cuisine']}, Rating: {row['rating']}")
    print(f"Nutrients: {row['nutrients']}\n")

conn.close()
