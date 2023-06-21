from flask import render_template, redirect, request, session, flash, Blueprint, url_for
from flask_app.models.user import User
from flask_app import Bcrypt

bcrypt = Bcrypt()

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/')
def show_register_form():
    return redirect(url_for('users.register_page'))

@users_bp.route('/register_page', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        session['inputted_user'] = {
            'username': request.form['username'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
        }
    user = session.get('inputted_user')
    return render_template('register.html', user=user)

@users_bp.route('/login_page')
def login_page():
    session.clear()
    return render_template('login.html')

@users_bp.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        session['inputted_user'] = {
            'username': request.form['username'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
        }
        return redirect(url_for('users.register_page'))

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'username': request.form['username'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = User.createUser(data)
    print(str(user_id) + " was created.")
    print(data)

    session['user_id'] = user_id
    session['Username'] = data['username']  
    session.pop('inputted_user', None)

    return redirect(url_for('recipes.recipes_page'))

@users_bp.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user = User.login(data)
    print("User:", str(user))
    if user is None:
        flash("Invalid email/password.")
        return render_template('login.html')
    print("User password:", user.password)
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email/password.")
        return render_template('login.html')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['logged_in'] = True
    print("Session:", session)
    return redirect(url_for('recipes.recipes_page'))


@users_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('users.login_page'))
