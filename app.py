from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from models import User  # Import the User model after db initialization

# Create tables and initial users
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password=generate_password_hash('adminpassword'),
            role='Admin'
        )
        normal_user = User(
            username='normal',
            password=generate_password_hash('normalpassword'),
            role='Normal'
        )
        dsu_user = User(
            username='dsu',
            password=generate_password_hash('dsupassword'),
            role='DSU'
        )
        rmu_user = User(
            username='rmu',
            password=generate_password_hash('rmupassword'),
            role='RM+WIP'
        )
        db.session.add(admin_user)
        db.session.add(normal_user)
        db.session.add(dsu_user)
        db.session.add(rmu_user)
        db.session.commit()

# Importing routes
import routes

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
