from flask import Blueprint, session
from . import mongo, bcrypt
from flask import request, redirect, url_for, flash, render_template
from datetime import datetime, timezone


auth = Blueprint('auth', __name__)
user_collection = mongo.db.users

@auth.route('/test-db')
def test_db():
    try:
        users_collection = user_collection
        return f"MongoDB connection successful!: {users_collection}"
    except Exception as e:
        return f"Error connecting to MongoDB: {str(e)}"
    

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_conf = request.form.get('password-conf')

        existing_user = user_collection.find_one({"email" : email})

        print(email, password, password_conf, existing_user)

        if existing_user:
          flash("Email already exists!")
          return redirect(url_for('auth.signup'))

        elif password == password_conf:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            user_data = ({
              'created_at': datetime.now(timezone.utc),
              'email': email,
              'password': hashed_password
            })

            user_collection.insert_one(user_data)

            flash("Account created!")
            return redirect(url_for('auth.login'))

        else:
            flash("Passwords does not match!")
            return redirect(url_for('auth.signup'))

    return render_template("signup.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = user_collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            session['user_id'] = str(user['_id'])
            print('Logged in successfully!', 'success')

            return redirect(url_for('views.home'))

        else:
            print('Login failed. Check your email or password.')

    return render_template("login.html")

@auth.route('/logout')
def logout():
  session.clear()
  flash('You have been logged out.')
  return redirect(url_for('auth.login'))