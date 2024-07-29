from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required
from app.models import Subject

main = Blueprint('main', __name__)

@main.route('/')
def home():
    subjects = Subject.query.all()
    return render_template('home.html', subjects=subjects)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

