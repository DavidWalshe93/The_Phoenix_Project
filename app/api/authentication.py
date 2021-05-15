"""
Author:     David Walshe
Date:       13 May 2021
"""

import logging

from flask import g, current_app  # Flask globals
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWS

from ..models import User
from .errors import unauthorized

# Setup authentication handlers.
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth("Bearer")
auth = MultiAuth(basic_auth, token_auth)

logger = logging.getLogger(__name__)


@basic_auth.verify_password
def verify_password(email_or_token: str, password: str) -> bool:
    """Top level function used for decorator, implementation found in "_verify_password"."""
    # Secondary method used to simplify unit testing.
    return _verify_password(email_or_token, password)


def _verify_password(email: str, password: str) -> bool:
    """
    Verifies a user's email and password combination for API access.

    :param email: The user email to identify and check credentials for or an authentication token.
    :param password: The user password to verify.
    :return: True if credentials were correct else False.
    """
    # Get the user information from the DB.
    user = User.query.filter_by(email=email).first()

    # If the user does not exist in the DB, return False.
    if not user:
        return False

    # Set flask global state.
    set_globals(token_used=False)

    logger.debug("Authorized with Email/Password.")

    # Check if the users password is correct.
    return user.verify_password(password=password)


@token_auth.verify_token
def verify_token(token: str):
    """
    Verifies a user's Bearer token for API access.

    :param token: The token supplied by the client.
    :return: True if the token identified user is not None, else False.
    """
    # Generate JWT signer.
    jws = JWS(current_app.config["SECRET_KEY"], current_app.config["TOKEN_EXPIRY"])
    logger.debug(f"{jws}")
    try:
        data = jws.loads(token)
    except Exception as err:
        logger.debug(f"{err}")
        return False

    # Set flask global state.
    set_globals(token_used=True)

    # Return active user.
    user = User.user_from_email(data)

    if user is not None:
        logger.debug("Authorized with Token.")
    else:
        logger.warning(f"Authentication failed.")

    return User.user_from_email(data)


def set_globals(token_used: bool) -> None:
    """
    Sets the Flask globals depending on token or password usecase.

    :param token_used: Boolean to state if a token was used for authentication.
    """
    g.token_used = token_used


@basic_auth.error_handler
def basic_auth_error():
    """Callback for failed authentication requests."""
    logger.debug("Basic authentication failed.")
    return unauthorized("Invalid credentials.")


@token_auth.error_handler
def token_auth_error():
    """Callback for failed authentication requests."""
    logger.debug("Token authentication failed.")
    return unauthorized("Invalid credentials.")
