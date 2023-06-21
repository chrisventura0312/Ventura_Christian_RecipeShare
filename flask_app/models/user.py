from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        if isinstance(data, list):
            data = data[0]
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def login(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        print(query)
        results = connectToMySQL('recipe_share_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def createUser(cls, data):
        query = "INSERT INTO users (username, first_name, last_name, email, password) VALUES (%(username)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipe_share_schema').query_db(query, data)

    @classmethod
    def getUserById(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipe_share_schema').query_db(query, data)
        print("results are"+ str(results))
        return cls(results)

    
    @staticmethod
    def is_email_taken(data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipe_share_schema').query_db(query, data)
        return len(results) > 0
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['username']) < 3:
            flash("Username must be at least 3 characters long.")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters long.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters long.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if User.is_email_taken(user):
            flash("Email address already in use.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        if not re.search(r"\d", user['password']):
            flash("Password must contain at least one number.")
            is_valid = False
        if not re.search(r"[A-Z]", user['password']):
            flash("Password must contain at least one uppercase letter.")
            is_valid = False
        return is_valid
    
    
    #Add an additional validation on passwords to have a least 1 number and 1 uppercase letter
    