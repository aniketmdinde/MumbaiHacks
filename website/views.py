from flask import Blueprint, redirect, url_for, session, render_template


views = Blueprint('views', __name__)

@views.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.signup'))
    
    return render_template("chat.html")