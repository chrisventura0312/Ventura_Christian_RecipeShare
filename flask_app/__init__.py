from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt
from flask_app.controllers.users import users_bp
from flask_app.controllers.recipes import recipes_bp
from flask_app.models.user import User



app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "secret_key"

@app.route('/')
def register_page():
    return redirect(url_for('users.register_page'))

app.register_blueprint(users_bp)
app.register_blueprint(recipes_bp)
