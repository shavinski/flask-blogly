"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def show_home():
    """ Display home page """

    return redirect('/users')

@app.get('/users')
def show_allUsers():
    """Display all users"""

    #TODO: order by name on the database, add docstrings for each view function

    users = User.query.all()
    return render_template("all_users.html", users = users)

@app.get('/users/new')
def show_form():
    """Deiplay new user form"""

    return render_template("new_user_form.html")

@app.post('/users/new')
def add_user():
    """Add new user and redirect to all users page"""
    #grab data from user input
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    #add a new user
    user = User (first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def load_userid_page(user_id):
    """Display user detail page"""
    user = User.query.get(user_id)
    posts = user.posts

    return render_template('user_detail.html', user = user, posts = posts)

@app.get('/users/<int:user_id>/edit')
def load_user_edit(user_id):
    """Display user edit form"""
    user = User.query.get(user_id)

    return render_template('edit_user.html', user = user)

@app.post('/users/<int:user_id>/edit')
def submit_updated_info(user_id):
    """Edit user information and redirect to user detail page"""
    user = User.query.get(user_id)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']


    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user and redirect to all users page"""
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show new post form"""
    user = User.query.get(user_id)

    return render_template("new_post_form.html", user=user)

@app.post('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Add a new post"""
    title = request.form['title']
    content = request.form['content']

    post = Post (title = title, content = content, user_code = user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.get('/posts/<int:post_id>')
def load_individual_post(post_id):
    """Loads page for the post selected"""

    post = Post.query.get(post_id)

    return render_template('individual_post.html', post = post)

@app.get('/posts/<int:post_id>/edit')
def load_edit_post_form(post_id):
    """ Load edit form page template"""

    post = Post.query.get(post_id)

    return render_template('edit_post.html', post = post)

@app.post('/posts/<int:post_id>/edit')
def update_post_info(post_id):
    """Updates post info in database and webpage"""
    post = Post.query.get(post_id)

    title = request.form['title']
    content = request.form['content']

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete an individual post"""

    post = Post.query.get(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')









