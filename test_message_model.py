"""Message model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()


class MessageModelTestCase(TestCase):
    """Test message model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        user1 = User(
            username="testuser1",
            password="password",
            email="testing@testing.com"
        )

        user2 = User(
            username="testuser2",
            password="password2",
            email="testing2@testing.com"
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        u1 = User.query.filter_by(username="testuser1").first()
        u2 = User.query.filter_by(username="testuser2").first()

        self.user1 = u1
        self.user2 = u2

        message1 = Message(
            text="test message 1",
            user_id=u1.id
        )

        message2 = Message(
            text="test message 2",
            user_id=u2.id
        )

        db.session.add(message1)
        db.session.add(message2)
        db.session.commit()

        self.client = app.test_client()


    def tearDown(self):
        db.session.rollback()


    def test_message_model(self):
        """Does model work?"""

        m = Message(
            text="message message",
            user_id=self.user1.id
        )

        db.session.add(m)
        db.session.commit()

        message = Message.query.filter_by(text="message message").first()

        self.assertTrue(message)


    def test_message_associates_with_user(self):
        """Is message associated with user?"""

        m = Message(
            text="test123",
            user_id=self.user2.id
        )

        db.session.add(m)
        db.session.commit()

        message = Message.query.filter_by(text="test123").first()

        self.assertEqual(message.user_id, self.user2.id)


    def test_add_message_invalid_user(self):
        """Error if invalid user on add message?"""

        try:
            m = Message(
                text="test456",
                user_id=999999
            )

            db.session.add(m)
            db.session.commit()

        except exc.IntegrityError:
            pass
            

    def test_too_many_characters_new_message(self):
        """Fail add message if too many characters?"""

        try:
            m = Message(text="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabcde", user_id=self.user1.id)

            db.session.add(m)
            
        except exc.DataError:
            pass