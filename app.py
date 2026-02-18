from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    query = ""
    recipes = []

    conn = sqlite3.connect("recipes.db")
    cur = conn.cursor()

    if request.method == "POST":
        query = request.form.get("query")
        # Search by title or cuisine
        cur.execute("""
            SELECT title, cuisine, rating 
            FROM recipes
            WHERE title LIKE ? OR cuisine LIKE ?
        """, (f"%{query}%", f"%{query}%"))
        recipes = cur.fetchall()
    else:
        # All recipes
        cur.execute("SELECT title, cuisine, rating FROM recipes")
        recipes = cur.fetchall()

    conn.close()
    return render_template("index.html", recipes=recipes, query=query)

if __name__ == "__main__":
    app.run(debug=True)
