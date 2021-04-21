# Auth Blueprint
from datetime import timedelta

from flask import Blueprint, render_template, flash, redirect, url_for, request, session, abort
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from wtforms import ValidationError
from urllib.parse import urlparse, urljoin

from my_app.auth.forms import SignupForm, LoginForm
from my_app import db, login_manager
from my_app.models import User


# Checks if the redirect url is safe (to prevent attackers from redirecting to a phising website)
def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


# SIGN UP BP
signup_bp = Blueprint('signup_bp', __name__, url_prefix='/signup')


@signup_bp.route('/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.username}. You have successfully signed up. Please login to continue.")
        except IntegrityError:
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('signup_bp.signup'))

        return redirect(url_for('login_bp.login'))
    return render_template('signup.html', title='Sign Up', form=form)


# LOGIN BP
login_bp = Blueprint('login_bp', __name__, url_prefix='/login')


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = form.password
        # Used for 'remember me' functionality, minutes define time before user is logged out
                # User and password validator
        if user is not None:
            if User.check_password(user, password.data):
                login_user(user)
                next = request.args.get('next')
                if not is_safe_url(next):
                    return abort(400)
                else:
                    flash(f"Hello, {user.username}. You have successfully logged in.")
                    return redirect(url_for('home_bp.index', name='user.username'))
    return render_template('login.html', title='Login', form=form)


# Logout BP
logout_bp = Blueprint('logout_bp', __name__, url_prefix='/logout')


@logout_bp.route('/')
@login_required
def logout():
    logout_user()
    flash(f'You have successfully logged out.')
    return redirect(url_for('home_bp.index'))


# Takes a user ID and returns a user object or None if the user does not exist
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


# Redirect unauthorized users to Login page
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login_bp.login'))
