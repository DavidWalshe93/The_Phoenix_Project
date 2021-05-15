"""
Author:     David Walshe
Date:       13 May 2021
"""

import logging
from typing import Union

from flask import g  # Flask globals
from flask_httpauth import HTTPBasicAuth

from ..models import User
from .errors import unauthorized

auth = HTTPBasicAuth()

logger = logging.getLogger(__name__)


@auth.verify_password
def verify_password(email_or_token: str, password: str) -> bool:
    """Top level function used for decorator, implementation found in "_verify_password"."""
    # Secondary method used to simplify unit testing.
    return _verify_password(email_or_token, password)


def _verify_password(email_or_token: str, password: str) -> bool:
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
        logger.debug(f"Authorized with Token.")
        return auth_with_token(token=email_or_token)

    logger.debug(f"Authorized with Email/Password.")
    return auth_with_password(email=email_or_token, password=password)


def auth_with_token(token: str) -> bool:
    """
    Setup the session with token authentication.

    :param token: The token supplied by the client.
    :return: True if the token identified user is not None, else False.
    """
    set_globals(token_or_user=token)

    return g.current_user is not None


def auth_with_password(email: str, password: str) -> bool:
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
    set_globals(token_or_user=user)

    # Check if the users password is correct.
    return user.verify_password(password=password)


def set_globals(token_or_user: Union[str, User]) -> None:
    """
    Sets the Flask globals depending on token or password usecase.

    :param token_or_user: A User object or a token string.
    """
    if isinstance(token_or_user, str):
        # Uses a token to id a User.
        g.current_user = User.verify_auth_token(token_or_user)
        g.token_used = True
    else:
        # User already ID'd from email
        g.current_user = token_or_user
        g.token_used = False


@auth.error_handler
def auth_error():
    """Callback for failed authentication requests."""
    return unauthorized("Invalid user credentials to access resource.")
