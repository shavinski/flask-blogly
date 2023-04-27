"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "https://cdn.digitbin.com/wp-content/uploads/Intentionally-created-Blank-Profile.jpg"

db = SQLAlchemy() #create a SQLAlchemy instance
#create a function that ties your db object to your app object
#thus, allows your flask app to connect to the specified db

def connect_db(app):
   """Connect to database."""
   app.app_context().push()
   db.app = app
   db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True)

    first_name = db.Column(
        db.String(35),
        nullable = False)

    last_name = db.Column(
        db.String(35),
        nullable = False)

    image_url = db.Column(
        db.Text,
        nullable = False,
        default = DEFAULT_IMAGE_URL)
