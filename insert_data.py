import sqlite3
import json
import math

# Connect DB
conn = sqlite3.connect("recipes.db")
cur = conn.cursor()

# JSON file la 1000+ recipes irukku nu assume pannrom
with open("large_recipes.json", "r", encoding="utf-8") as f:
    recipes = json.load(f)

for recipe in recipes:
    rating = recipe.get("rating")
    rating = None if rating is None or (isinstance(rating, float) and math.isnan(rating)) else rating

    prep_time = recipe.get("prep_time")
    prep_time = None if prep_time is None or (isinstance(prep_time, float) and math.isnan(prep_time)) else prep_time

    cook_time = recipe.get("cook_time")
    cook_time = None if cook_time is None or (isinstance(cook_time, float) and math.isnan(cook_time)) else cook_time

    total_time = recipe.get("total_time")
    total_time = None if total_time is None or (isinstance(total_time, float) and math.isnan(total_time)) else total_time

    nutrients = json.dumps(recipe.get("nutrients") or {})

    cur.execute("""
        INSERT INTO recipes
        (cuisine, title, rating, prep_time, cook_time, total_time, description, nutrients, serves)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recipe.get("cuisine"),
        recipe.get("title"),
        rating,
        prep_time,
        cook_time,
        total_time,
        recipe.get("description"),
        nutrients,
        recipe.get("serves")
    ))

conn.commit()
conn.close()
print("All 1000+ recipes inserted successfully.")
