from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User
import re



class Recipe:
    schema = "recipe_share_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def createRecipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under_30, date_made, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(users_id)s);"
        return connectToMySQL(cls.schema).query_db(query, data)

    @classmethod
    def get_all_recipes_with_creator(cls):
        query='SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.users_id;'
        results = connectToMySQL(cls.schema).query_db(query)
        recipes = []
        for recipe in results:
            one_recipe = cls(recipe)
            cook_info= {
                "id": recipe['users.id'],
                "username": recipe['username'],
                "first_name": recipe['first_name'],
                "last_name": recipe['last_name'],
                "email": recipe['email'],
                "password": recipe['password'],
                "created_at": recipe['users.created_at'],
                "updated_at": recipe['users.updated_at']
            }
            cook=User(cook_info)
            one_recipe.user=cook
            one_recipe.date_made = recipe['date_made']
            recipes.append(one_recipe)
        return recipes
    
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.users_id WHERE recipes.id = %(id)s;"
        data = {
            "id": id
        }
        result = connectToMySQL(cls.schema).query_db(query, data)
        recipe = cls(result[0])
        cook_info= {
                "id": result[0]['users.id'],
                "username": result[0]['username'],
                "first_name": result[0]['first_name'],
                "last_name": result[0]['last_name'],
                "email": result[0]['email'],
                "password": result[0]['password'],
                "created_at": result[0]['users.created_at'],
                "updated_at": result[0]['users.updated_at']
            }
        cook=User(cook_info)
        recipe.user=cook
        return recipe
    
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s WHERE id = %(id)s;"
        return connectToMySQL(cls.schema).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {
            "id": id
        }
        return connectToMySQL(cls.schema).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.")
            is_valid = False
        if not recipe['under_30']:
            flash("Please select whether this recipe takes less than 30 minutes to make.")
            is_valid = False
        if len(recipe['date-made']) < 1:
            flash("Please select a date.")
            is_valid = False
        else:
            date_pattern = r"\d{2}-\d{2}-\d{4}"
            if not re.match(date_pattern, recipe['date-made']):
                flash("Please select a valid date.")
                is_valid = False
        return is_valid
    
    
    