import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )
        db.session.add(test_user)
        db.session.commit()
        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test showing all users"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_show_form(self):
        """Test showing new user form"""
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Testing for show_form -->", html)

    def test_redirection_newUserForm(self):
        """Test redirect to the user list after adding user info"""
        with self.client as c:
            resp = c.post("/users/new",
                          data = {"first_name": 'test1_first',
                                                "last_name": 'test1_last',
                                                "image_url": DEFAULT_IMAGE_URL})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_redirection_followed_newUserForm(self):
        """Test new user info reflected in the all users page"""
        with app.test_client() as client:
            resp = client.post("/users/new",
                               data = {"first_name": 'test1_first',
                                       "last_name": 'test1_last',
                                       "image_url": DEFAULT_IMAGE_URL}
                                       ,follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

#TODO: add test for delete users (use assertNotIn)
    def test_user_delete(self):
        """Test if user is deleted and its info not showing in all users page"""
        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test1_first", html)
            self.assertNotIn("test1_last", html)

    def test_user_edit(self):
        """Test for editing a user information"""
        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/edit",
                           data = {"first_name": 'test_change_first',
                                   "last_name": 'test1_last',
                                   "image_url": DEFAULT_IMAGE_URL}
                                   ,follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertNotIn("test1_first", html)
            self.assertIn("test_change_first", html)


class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        Post.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )
        db.session.add(test_user)
        db.session.commit()
        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id



        test_post = Post(
            title="test_post_title",
            content="test_post_content",
            user_code=test_post.user.id, #FIXME: will this grab user id?
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_post_show_form(self):
        """Test showing new user form"""
        with self.client as c:
            resp = c.get("/users/<int:user_id>/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Testing for show_form -->", html)