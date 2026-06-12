from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.get_by_email(email)
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        try:
            new_user = User.create(name, email, generate_password_hash(password))
            login_user(new_user)
            return redirect(url_for('chat_interface'))
        except Exception as e:
            flash(f'Registration error: {str(e)}')
            return redirect(url_for('auth.register'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat_interface'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.get_by_email(email)

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('chat_interface'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
