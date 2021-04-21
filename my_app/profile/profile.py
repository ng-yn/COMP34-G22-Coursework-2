# Profile page
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

import my_app
from my_app import db
from my_app.profile.forms import ProfileForm
from my_app.models import Profile, User, Posts
import secrets, os

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


# @profile_bp.route('/')
# @login_required
# def index():
#     form = ProfileForm()
#     return render_template('profile.html', title="Profile", form=form)


@profile_bp.route('/', methods=['POST', 'GET'])
@login_required
def profile():
    profile = Profile.query.join(User).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('profile.update_profile'))
    else:
        return redirect(url_for('profile.create_profile'))


@profile_bp.route('/create_profile', methods=['POST', 'GET'])
@login_required
def create_profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        p = Profile(username=form.username.data, bio=form.bio.data, user_id=current_user.id, image_file='default.jpg')
        db.session.add(p)
        db.session.commit()
        flash('Profile created.')
        return redirect(url_for('profile.profile', username=p.username))
    return render_template('/newprofile.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('../my_app/static/profilepics/' + picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@profile_bp.route('/update_profile', methods=['POST', 'GET'])
@login_required
def update_profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    form = ProfileForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            profile.image_file = picture_file

        profile.bio = form.bio.data
        profile.username = form.username.data
        db.session.commit()
        'Profile updated.'
        return redirect(url_for('profile.profile', username=profile.username))
    image_file = url_for('static', filename='profilepics/' + profile.image_file)
    return render_template('profile.html', form=form, username=profile.username, userimage=image_file)


# @profile_bp.route('/display_profiles', methods=['POST', 'GET'])
# @profile_bp.route('/display_profiles/<username>', methods=['POST', 'GET'])
# @login_required
# def display_profiles(username=None):
#     results = None
#     if username is None:
#         if request.method == 'POST':
#             term = request.form['search_term']
#             if term == "":
#                 flash("Enter a name to search for")
#                 return redirect(url_for("profile.profile"))
#             results = Profile.query.filter(Profile.username.contains(term)).all()
#     else:
#         results = Profile.query.filter_by(username=username).all()
#     if results is None:
#         flash("Username not found.")
#         return redirect(url_for("profile.profile"))
#     return render_template('display_profile.html', profiles=results)

@profile_bp.route('/display_profiles', methods=['POST', 'GET'])
@login_required
def display_profiles():
    results = None
    if request.method == 'POST':
        search_term = request.form['search_term']
        if search_term == '':
            flash("Please enter a username to search for.")
            return redirect(url_for("community_bp.index"))
        else:
            results = Profile.query.filter(Profile.username.contains(search_term)).all()

    if results is None:
        flash("Username not found.")
        return redirect(url_for("community_bp.index"))
    return render_template('display_profile.html', profiles=results)


@profile_bp.route('/<username>')
@login_required
def user_profile(username):
    user = username
    exists = Profile.query.filter(Profile.username == user).first()
    if exists:
        bio = exists.bio
        image_file = exists.image_file
        a = Posts.query.filter_by(user_id=exists.user_id).all()
        return render_template('userprofile.html', user=user, bio=bio, image_file=image_file, posts=a)
    else:
        flash("That user does not exist")
        return redirect((url_for('community_bp.index')))


