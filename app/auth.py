from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .utils.database import get_db_connection
from . import login_manager
import sqlite3

auth = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('views.home'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
            
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', 
                         (username, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists.', 'danger')
            
    return render_template('register.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
