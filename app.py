import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database

db = SQL("sqlite:///cookbook.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():

    recipes = db.execute("SELECT id, title, instructions FROM Recipes")
    return render_template("index.html", recipes=recipes)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")

        #filter recipes through database based on keyword
        recipes = db.execute("SELECT id, title, instructions FROM Recipes WHERE title LIKE ?", keyword)

        return render_template("searched.html", recipes=recipes)

    else:
        return render_template("search.html")
def search(recipe_id):

    recipes = db.execute("SELECT title, instructions FROM Recipes WHERE id = ?", recipe_id)

    return render_template("searched.html", recipes=recipes)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):

    recipe = db.execute("SELECT * FROM Recipes WHERE id = ?", (recipe_id,))[0]

    ingredients = db.execute("SELECT name FROM Ingredients WHERE recipe_id=?", recipe_id)

    if recipe:
        return render_template("recipe.html", recipe=recipe, ingredients=ingredients)
    else:
        return "Recipe not found", 404

@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form.get("name")
        ingredients = request.form.getlist("ingredients")
        instructions = request.form.get("instructions")

        # Insert the new recipe
        db.execute("INSERT INTO Recipes (title, instructions) VALUES (?, ?)", name, instructions)
        result = db.execute("SELECT id FROM Recipes WHERE title=? AND instructions=?", name, instructions)[0]

        #extracting id from dictionary
        if result:
            recipeId = result['id']
        else:
            raise ValueError("Recipe not found.")

        #insert ingredients with linked recipe id
        for ingredient in ingredients:
            db.execute("INSERT INTO Ingredients (name, recipe_id) VALUES (?, ?)", ingredient, recipeId)

        return render_template("added.html", name=name, ingredients=ingredients, instructions=instructions)

    else:
        return render_template("add.html")

@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit(recipe_id):
    if request.method == "POST":

        print("error")
        new_name = request.form.get("name")
        new_ingredients = request.form.getlist("ingredients")
        new_instructions = request.form.get("instructions")

        #update db
        db.execute("UPDATE Recipes SET title = ?, instructions = ? WHERE id = ?",
            new_name, new_instructions, recipe_id)

        db.execute("DELETE FROM Ingredients WHERE recipe_id = ?", recipe_id)
        for ingredient in new_ingredients:
            db.execute("INSERT INTO Ingredients (name, recipe_id) VALUES (?, ?)", ingredient, recipe_id)

        recipe = db.execute("SELECT * FROM Recipes WHERE id = ?", recipe_id)

        if recipe:
            return redirect("/")
        else:
            return "Recipe Not Found", 404

    else:
        recipe = db.execute("SELECT title, instructions FROM Recipes WHERE id=?", recipe_id)[0]
        ingredients = db.execute("SELECT name FROM Ingredients WHERE recipe_id=?", recipe_id)

        return render_template("edit.html", recipe_id=recipe_id, recipe=recipe, ingredients=ingredients)

@app.route("/delete/<int:recipe_id>", methods=["GET", "POST"])
def delete(recipe_id):
    if request.method == "POST":

        db.execute("DELETE FROM Recipes WHERE id=?", recipe_id)

        return redirect("/")
    else:
        recipe = db.execute("SELECT title FROM Recipes WHERE id = ?", recipe_id)
        name = recipe[0]["title"]

        return render_template("delete.html", name=name, recipe_id=recipe_id)

