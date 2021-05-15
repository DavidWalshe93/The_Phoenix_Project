"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging
from typing import Union

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .. import db

logger = logging.getLogger(__name__)

auth = HTTPBasicAuth()


class User(UserMixin, db.Model):
    """Models a User object from a users SQL table."""
    __tablename__ = "users"

    # User columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    last_login = db.Column(db.DateTime)

    # ======================================================================================================================
    # Password Handling
    # ======================================================================================================================

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

    # ======================================================================================================================
    # Token Handling
    # ======================================================================================================================

    def generate_auth_token(self, expiration: int):
        """
        Generates an authentication token to replace password auth for users.

        :param expiration: The expiry time in seconds for the generated token.
        :return: A new authentication token.
        """
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)

        return dict(token=s.dumps({"id": self.id,
                                   "email": self.email,
                                   "password": self.password_hash}).decode("utf8"))

    @staticmethod
    def verify_auth_token(token) -> Union[object, None]:
        """
        Verifies an authentication token and returns its assigned user if valid.

        :param token: The token to verify.
        :return: Returns the user the token is for if the token is valid, else returns None.
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except Exception as err:
            logger.debug(f"Could not load token: {err}")
            return None

        # Get the identified user.
        user: User = User.query.get(data['id'])

        # Ensure the user's details have not been altered since the token was generated.
        if user.email == data["email"] and user.password_hash == data["password"]:
            return user
        else:
            return None

    # ======================================================================================================================
    # Helpers
    # ======================================================================================================================

    @property
    def already_exists(self) -> bool:
        """
        Check if the User already exists in the database.

        :return: Whether the User already exists.
        """
        if self.query.filter_by(email=self.email).first():
            return True
        else:
            return False

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

#
# @login_manager.user_loader
# def load_user(user_id: str):
#     """
#     Retrieves information on the logged in user.
#
#     :param user_id: The user id to load information from.
#     :return: The user object.
#     """
#     return User.query.get(int(user_id))
