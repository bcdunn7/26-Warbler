"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test user model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user1 = User.signup(
            username="testuser1",
            password="password",
            email="testing@testing.com",
            image_url=None
        )

        user2 = User.signup(
            username="testuser2",
            password="password2",
            email="testing2@testing.com",
            image_url=None
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.client = app.test_client()


    def tearDown(self):
        db.session.rollback()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    def test_user_repr(self):
        """Does repr work?"""

        user = User.query.first()

        self.assertEqual(str(user), f"<User #{user.id}: {user.username}, {user.email}>")

    
    def test_not_following(self):
        """Correctly detects not following?"""

        user1 = User.query.filter_by(username="testuser1").first()

        self.assertNotIn('user2', str(user1.following))


    def test_following(self):
        """Correctly detects following?"""

        user1 = User.query.filter_by(username="testuser1").first()
        user2 = User.query.filter_by(username="testuser2").first()

        follow = Follows(user_being_followed_id=f"{user2.id}", user_following_id=f"{user1.id}")

        db.session.add(follow)
        db.session.commit()

        self.assertIn('testuser2', str(user1.following))


    def test_is_not_followed(self):
        """Correctly detects not followed?"""

        user1 = User.query.filter_by(username="testuser1").first()

        self.assertNotIn('user2', str(user1.followers))


    def test_is_followed(self):
        """Correctly detects followed?"""

        user1 = User.query.filter_by(username="testuser1").first()
        user2 = User.query.filter_by(username="testuser2").first()

        follow = Follows(user_being_followed_id=f"{user2.id}", user_following_id=f"{user1.id}")

        db.session.add(follow)
        db.session.commit()

        self.assertIn('testuser1', str(user2.followers))

    def test_signup_user(self):
        """Created user?"""

        user = User.signup(
            username="testuser3",
            password="password3",
            email="testing3@test.com",
            image_url="image"
            )

        db.session.commit()

        user3 = User.query.filter_by(username="testuser3").first()

        self.assertEqual(user, user3)

        self.assertTrue(user3.password.startswith('$2b$'))


    def test_invalid_user_signup(self):
        """Error if invalid user?"""

        user = User.signup(
            username="testuser1",
            password="password3",
            email="testing3@test.com",
            image_url="image"
            )

        self.assertRaises(exc.InvalidRequestError)


    def test_authenticate(self):
        """Authenticates?"""

        user = User.authenticate(username="testuser1", password="password")

        self.assertTrue(user)


    def test_authenticate_incorrect_username(self):
        """Fail authentication when incorrect username?"""

        user = User.authenticate(username="INVALID", password="password")

        self.assertFalse(user)


    def test_authenticate_incorrect_password(self):
        """Fail authentication when incorrect password?"""

        user = User.authenticate(username="testuser1", password="INVALID")