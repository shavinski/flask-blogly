"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

    users = User.query.all()
    return render_template("all_users.html", users = users)

@app.get('/users/new')
def show_form():

    return render_template("new_user_form.html")

@app.post('/users/new')
def add_user():
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

    user = User.query.get(user_id)


    #TODO: Should we have only have the instance here, or should we have first_name = user.first_name, last_name = user.last_name etc
    return render_template('user_detail.html', user = user)

@app.get('/users/<int:user_id>/edit')
def load_user_edit(user_id):

    user = User.query.get(user_id)

    return render_template('edit_user.html', user = user)

@app.post('/users/<int:user_id>/edit')
def submit_updated_info(user_id):

    user = User.query.get(user_id)

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']


    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# @app.get('/users/<int:user_id>/delete')
# def reload_users_page(user_id):



