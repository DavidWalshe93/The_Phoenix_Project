"""
Author:     David Walshe
Date:       13 May 2021
"""

import logging

from flask import g
from flask_httpauth import HTTPBasicAuth

from ..models import User
from .errors import unauthorized

# auth = HTTPBasicAuth()
auth = HTTPBasicAuth()

logger = logging.getLogger(__name__)


@auth.verify_password
def verify_password(email_or_token: str, password: str) -> bool:
    """
    Verifies a user's email and password combination or validates a authentication token assigned by the user.

    :param email_or_token: The user email to identify and check credentials for or an authentication token.
    :param password: The user password to verify.
    :return: True if credentials were correct else False.
    """
    # Check if the user supplied a email or a token, if anonymous user, return false.
    if email_or_token == "":
        logger.debug(f"No email or token provided.")
        return False

    if password == "":
        logger.debug(f"Token provided.")
        return token_auth(token=email_or_token)

    logger.debug(f"Email/Password provided.")
    return password_auth(email=email_or_token, password=password)


def token_auth(token: str) -> bool:
    """
    Setup the session with token authentication.

    :param token: The token supplied by the client.
    :return: True if the token identified user is not None, else False.
    """
    g.current_user = User.verify_auth_token(token)
    g.token_used = True

    return g.current_user is not None


def password_auth(email: str, password: str) -> bool:
    """
    Setup the session with email/password authentication.

    :param email: The email address supplied by the user.
    :param password: The password supplied by the user.
    :return: If the email/password combination is valid.
    """
    # Get the user information from the DB.
    user = User.query.filter_by(email=email).first()

    # If the user does not exist in the DB, return False.
    if not user:
        return False

    # Add the user to the Flask globals for this session.
    g.current_user = user
    g.token_used = False

    # Check if the users password is correct.
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    """Callback for failed authentication requests."""
    return unauthorized("Invalid user credentials to access resource.")
