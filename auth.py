from flask import Blueprint, render_template, request, redirect, url_for,flash
from models import User
from flask_login import login_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for('profile'))