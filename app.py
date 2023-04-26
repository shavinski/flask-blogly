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

    return render_template("all_users.html")

@app.get('/users/new')
def show_form():

    return render_template("new_user_form.html")

@app.post('/users/new')
def add_user():
    #grab data from user input
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    #add a new user
    user = User (first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')