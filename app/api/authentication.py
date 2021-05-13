"""
Author:     David Walshe
Date:       13 May 2021
"""

import logging

from flask import g
from flask_httpauth import HTTPBasicAuth

from ..models import User

auth = HTTPBasicAuth()

logger = logging.getLogger(__name__)


@auth.verify_password
def verify_password(email: str, password: str) -> bool:
    """
    Verifies a user's email and password combination.

    :param email: The user email to identify and check credentials for.
    :param password: The user password to verify.
    :return: True if credentials were correct else False.
    """
    # Check if the user supplied a email, if anonymous user, return false.
    if email == "":
        return False

    # Get the user information from the DB.
    user = User.query.filter_by(email=email).first()

    # If the user does not exist in the DB, return False.
    if not user:
        return False

    # Add the user to the Flask globals for this session.
    g.current_user = user

    # Check if the users password is correct.
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    """Callback for failed authentication requests."""
    return unauthorized("Invalid user credentials")
