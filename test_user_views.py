"""User View tests."""

import os
from typing import Type
from unittest import TestCase

from models import db, connect_db, Message, User, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test2.com",
                                    password="testuser2",
                                    image_url=None)

        self.testuser.id = 1
        self.testuser2.id = 2

        db.session.commit()

        follow1 = Follows(user_being_followed_id=1, user_following_id=2)

        follow2 = Follows(user_being_followed_id=2, user_following_id=1)

        db.session.add(follow1)
        db.session.add(follow2)

        db.session.commit()

    
    # def test_list_users(self):
    #     """Show list of users?"""

    #     with self.client as c:
    #         resp = c.get('/users')

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("@testuser", str(resp.data))


    # def test_list_users_if_none(self):
    #     """View if no users?"""

    #     User.query.delete()

    #     with self.client as c:
    #         resp = c.get('/users')

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("<h3>Sorry, no users found</h3>", str(resp.data))

    
    # def test_show_user_details(self):
    #     """Show user details?"""

    #     with self.client as c:
    #         resp = c.get('/users/1')

    #     self.assertEqual(resp.status_code, 200)

    #     self.assertIn("@testuser", str(resp.data))


    # def test_invalid_user_details(self):
    #     """404 if invalid user?"""

    #     with self.client as c:
    #         resp = c.get('/users/12345678')

    #         self.assertEqual(resp.status_code, 404)

    
    # def test_show_user_following(self):
    #     """Show user following?"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         resp = c.get("/users/1/following")

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("Unfollow", str(resp.data))

    # def test_show_user_following_invalid_user(self):
    #     """Show unauthorized if invalid user for user following?"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = 12345678

    #         resp = c.get("/users/1/following", follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("unauthorized", str(resp.data))


    # def test_show_user_following_no_user(self):
    #     """Show unauthorized if no user for user following?"""

    #     with self.client as c:

    #         resp = c.get("/users/1/following", follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("unauthorized", str(resp.data))


    # def test_show_user_followers(self):
    #     """Show user followers?"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         resp = c.get("/users/1/followers")

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("Follow", str(resp.data))

    # def test_show_user_followers_invalid_user(self):
    #     """Show unauthorized if invalid user for user followers?"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = 12345678

    #         resp = c.get("/users/1/followers", follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("unauthorized", str(resp.data))


    # def test_show_user_followers_no_user(self):
    #     """Show unauthorized if no user for user followers?"""

    #     with self.client as c:

    #         resp = c.get("/users/1/following", follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("unauthorized", str(resp.data))


    # def test_show_user_likes(self):
    #     """Show user likes?"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         resp = c.get("/users/1/likes")

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("col-sm-6", str(resp.data))

    # def test_show_user_likes_invalid_user(self):
    #     """Show unauthorized if invalid user for user likes?"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = 12345678

    #         resp = c.get("/users/1/likes", follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("unauthorized", str(resp.data))


    # def test_show_user_likes_no_user(self):
    #     """Show unauthorized if no user for user likes?"""

    #     with self.client as c:

    #         resp = c.get("/users/1/likes", follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)

    #         self.assertIn("unauthorized", str(resp.data))


    def test_add_follow(self):
        """Add follow?"""

        Follows.query.delete()
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post('/users/follow/2', follow_redirects=True)

            follow = Follows.query.first()

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(follow.user_being_followed_id, 2)

            self.assertIn("testuser2", str(resp.data))


    def test_add_follow_invalid_user(self):
        """Show unauthorized if invalid user for add follow?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 12345678

            resp = c.post('/users/follow/2', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("unauthorized", str(resp.data))


    def test_add_follow_no_user(self):
        """Show unauthorized if no user for add follow?"""

        with self.client as c:

            resp = c.post('/users/follow/2', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("unauthorized", str(resp.data))

            
    def test_unfollow(self):
        """Can unfollow?"""
    
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post('/users/stop-following/2', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            follow = Follows.query.filter_by(user_following_id=1).first()

            self.assertIsNone(follow)

# ******************************************

### ERROR ###
    # def test_invalid_unfollow(self):
    #     """Error if invalid follow?"""

    #     # with self.client as c:
    #     #     with c.session_transaction() as sess:
    #     #         sess[CURR_USER_KEY] = self.testuser.id

    #     #     # resp = c.post('/users/stop-following/1', follow_redirects=True)
    #     with app.app_context():
    #         with self.assertRaises(ValueError):
    #             app.stop_following(1)

    #             #Error: Flask has no stop_following

# *********************************************

    def test_unfollow_invalid_user(self):
        """Show unauthorized if invalid user for unfollow?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 12345678

            resp = c.post('/users/stop-following/2', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("unauthorized", str(resp.data))


    def test_unfollow_no_user(self):
        """Show unauthorized if no user for unfollow?"""

        with self.client as c:

            resp = c.post('/users/stop-following/2', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("unauthorized", str(resp.data))
