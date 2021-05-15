"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging
from typing import Union, Dict, Any
from collections import OrderedDict

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .. import db

logger = logging.getLogger(__name__)


class User(db.Model):
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
                                   "password_hash": self.password_hash}).decode("utf8"))

    @staticmethod
    def user_from_token_props(data: Dict[str, Any]) -> Union[object, bool]:
        """
        Finds and returns a user identified by a token.

        :param data: A dictionary object containing an email and password_hash field.
        :return: A User object if a user was found for the email and password supplied, else False.
        """
        # Check that an email property exists on the data passed.
        email = data.get("email")
        password_hash = data.get("password_hash")

        # Ensure values exist.
        if not all([email, password_hash]):
            logger.warning(f"Data missing properties.")
            return None

        # Get the identified user.
        user: User = User.query.filter_by(email=email).first()

        # If no matching user is returned.
        if user is None:
            return None

        # Ensure the user's details have not been altered since the token was generated.
        if user.email == email and user.password_hash == password_hash:
            return user
        else:
            return None

    @staticmethod
    def user_from_email(email: str) -> Union[object, bool]:
        """
        Finds and returns a user identified by their email.

        :param email: A user's email.
        :return: A User object if a user was found for the email supplied, else False.
        """
        # Get the identified user.
        return User.query.filter_by(email=email).first()

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
        return OrderedDict(
            id=self.id,
            name=self.name,
            email=self.email,
            last_login=self.last_login
        )

    def __repr__(self) -> str:
        """Return string representation of User object."""
        return f"<User {self.name} - {self.last_login}>"
