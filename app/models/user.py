"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .. import db

logger = logging.getLogger(__name__)


class User(UserMixin, db.Model):
    """Models a User object from a users SQL table."""
    __tablename__ = "users"

    # User columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    last_login = db.Column(db.DateTime)

    @property
    def password(self):
        """Plain text password access should raise error."""
        raise AttributeError("For security purposes, 'password' is not a readable attribute.")

    @password.setter
    def password(self, password: str):
        """Converts the plain-text password into a salted hash before storing in the database."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Verifies the user password against a salted hash within the database.

        :param password: The password to verify.
        :return: True if password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def as_dict(self) -> dict:
        """
        Returns dictionary representation of object, useful for JSON encoding.
        """
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
            last=self.last_login
        )

    def __repr__(self) -> str:
        """Return string representation of User object."""
        return f"<User {self.name} - {self.last_login}>"
