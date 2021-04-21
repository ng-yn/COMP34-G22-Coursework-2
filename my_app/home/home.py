# Home Page
from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import current_user

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/', defaults={'name': 'Anonymous'})
@home_bp.route('/<name>')
def index(name):
    if not current_user.is_anonymous:
        name = current_user.username
    return render_template('home.html', title='Home Page', name=name)

