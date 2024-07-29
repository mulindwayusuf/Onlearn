from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.forms import RegistrationForm, LoginForm
from app.models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
         # Check if email already exists
        existing_user_username = User.query.filter_by(username=form.username.data).first()
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_username:
            flash('Username already taken, choose another one', 'danger')
            return redirect(url_for('auth.register'))
        if existing_user_email:
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(username=form.username.data, email=form.email.data, role= 'user')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful', 'success')
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
