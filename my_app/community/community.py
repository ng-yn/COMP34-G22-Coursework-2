# Community Page
from werkzeug.exceptions import abort
from my_app.models import Posts, Profile, User
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from datetime import datetime
from my_app import db

community_bp = Blueprint('community_bp', __name__, url_prefix='/community')


@community_bp.route('/')
@login_required
def index():
    posts = Posts.query.all()
    posts.reverse()
    users = User.query.all()
    return render_template('community.html', title='Welcome to the Community Section', posts=posts, users=users)


@community_bp.route('/<int:post_id>')
def post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    profile = Profile.query.filter_by(user_id=post.user_id).first()
    if post is None:
        abort(404)
    return render_template('post.html', post=post, profile=profile)


@community_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            post = Posts(title=title, content=content, created=datetime.utcnow(), user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('community_bp.index'))
    return render_template('create.html')


@community_bp.route('/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(post_id):
    post = Posts.query.filter_by(id=post_id).first()

    if post.user_id != current_user.id:
        abort(403)

    if post is None:
        abort(404)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            post.title = title
            post.content = content
            db.session.commit()
            return redirect(url_for('community_bp.index'))

    return render_template('edit.html', post=post)


@community_bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('community_bp.index'))
