from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sqlite3
import json
from typing import Optional

app = FastAPI(title="Recipes API")

# Serve frontend from / (static folder)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Helper function to connect DB
def get_db():
    conn = sqlite3.connect("recipes.db")
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# --------------------
# Endpoint 1: Get all recipes (paginated, sorted by rating)
# --------------------
@app.get("/api/recipes")
def get_recipes(page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM recipes")
    total = cur.fetchone()[0]

    cur.execute("SELECT * FROM recipes ORDER BY rating DESC LIMIT ? OFFSET ?", (limit, offset))
    rows = cur.fetchall()
    data = []
    for row in rows:
        d = dict(row)
        d['nutrients'] = json.loads(d['nutrients'])
        data.append(d)

    conn.close()
    return {"page": page, "limit": limit, "total": total, "data": data}

# --------------------
# Endpoint 2: Search recipes
# --------------------
@app.get("/api/recipes/search")
def search_recipes(
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    calories: Optional[str] = None,
    total_time: Optional[str] = None,
    rating: Optional[str] = None
):
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if cuisine:
        query += " AND cuisine LIKE ?"
        params.append(f"%{cuisine}%")
    if rating:
        if rating.startswith(">="):
            query += " AND rating >= ?"
            params.append(float(rating[2:]))
        elif rating.startswith("<="):
            query += " AND rating <= ?"
            params.append(float(rating[2:]))
        elif rating.startswith(">"):
            query += " AND rating > ?"
            params.append(float(rating[1:]))
        elif rating.startswith("<"):
            query += " AND rating < ?"
            params.append(float(rating[1:]))
        else:
            query += " AND rating = ?"
            params.append(float(rating))
    if total_time:
        if total_time.startswith(">="):
            query += " AND total_time >= ?"
            params.append(int(total_time[2:]))
        elif total_time.startswith("<="):
            query += " AND total_time <= ?"
            params.append(int(total_time[2:]))
        elif total_time.startswith(">"):
            query += " AND total_time > ?"
            params.append(int(total_time[1:]))
        elif total_time.startswith("<"):
            query += " AND total_time < ?"
            params.append(int(total_time[1:]))
        else:
            query += " AND total_time = ?"
            params.append(int(total_time))

    # Calories filter
    if calories:
        operator = calories[:2] if calories[:2] in ["<=", ">="] else calories[0]
        value = int(calories[2:] if operator in ["<=", ">="] else calories[1:] if operator in ["<", ">"] else calories)
        cur.execute("SELECT * FROM recipes")
        rows = cur.fetchall()
        filtered = []
        for row in rows:
            nutrients = json.loads(row['nutrients'])
            cal_str = nutrients.get("calories", "0").split()[0].replace(",", "")
            cal_val = int(cal_str)

            if operator == "<=" and cal_val <= value:
                filtered.append(row)
            elif operator == ">=" and cal_val >= value:
                filtered.append(row)
            elif operator == "<" and cal_val < value:
                filtered.append(row)
            elif operator == ">" and cal_val > value:
                filtered.append(row)
            elif operator == "=" and cal_val == value:
                filtered.append(row)
        rows = filtered
    else:
        cur.execute(query, params)
        rows = cur.fetchall()

    data = []
    for row in rows:
        d = dict(row)
        d['nutrients'] = json.loads(d['nutrients'])
        data.append(d)

    conn.close()
    return {"data": data}
