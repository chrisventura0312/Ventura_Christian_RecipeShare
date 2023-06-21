from flask import render_template, redirect, request, session, flash, Blueprint, url_for
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipes_bp.route('/' , methods=['GET'])
def recipes_page():
    if 'user_id' not in session:
        flash("Please log in.")
        return redirect(url_for('users.login_page'))
    data = {
        'id': session['user_id']
    }
    recipes = Recipe.get_all_recipes_with_creator()
    user = User.getUserById(data)
    return render_template('recipes.html', user=user, recipes=recipes)

@recipes_bp.route('/<int:id>', methods=['GET', 'POST'])
def show_recipe(id):
    recipe = Recipe.get_one(id)
    user= User.getUserById({'id': recipe.users_id})
    return render_template('view_recipe.html', recipe=recipe, user=user)

@recipes_bp.route('/create')
def create_recipe():
    if 'user_id' not in session:
        flash("Please log in.")
        return redirect(url_for('users.login_page'))
    print (session['user_id'])
    data = {
        'id': session['user_id']
    }
    user = User.getUserById(data)
    return render_template('create_recipe.html', user=user, recipes=[])

@recipes_bp.route('/new', methods=['POST'])
def new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(url_for('recipes.create_recipe'))
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30': request.form['under_30'],
        'date_made': request.form['date-made'],  
        'users_id': session['user_id']
    }   
    recipe_id = Recipe.createRecipe(data)
    print(str(recipe_id) + " was created.")
    return redirect(url_for('recipes.recipes_page'))

@recipes_bp.route('/<int:id>/edit')
def edit_recipe(id):
    recipe = Recipe.get_one(id)
    return render_template('edit_recipe.html', recipe=recipe)

@recipes_bp.route('/<int:id>/update', methods=[ 'POST'])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return render_template('edit_recipe.html', recipe=Recipe.get_one(id))
    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30': request.form['under_30'],
        'date_made': request.form['date-made'],
        'users_id': session['user_id']
    }
    Recipe.update(data)
    return render_template('view_recipe.html', recipe=Recipe.get_one(id))


@recipes_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_recipe(id):
    Recipe.delete(id)
    return redirect(url_for('recipes.recipes_page'))
