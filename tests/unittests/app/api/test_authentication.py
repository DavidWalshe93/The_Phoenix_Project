"""
Author:     David Walshe
Date:       14 May 2021
"""

from unittest.mock import patch

import pytest

from app.models import User
import app.api.authentication as sut


def test_verify_password_no_email_or_token(caplog):
    """
    :GIVEN: No username, token or password.
    :WHEN:  Verifying a users credentials.
    :THEN:  Verify the verification fails due to no email/token being supplied.
    """
    # Target paths of functions to mock.
    auth_token_target = "app.api.authentication.auth_with_token"
    auth_password_target = "app.api.authentication.auth_with_password"

    with patch(auth_token_target) as mock_token:
        with patch(auth_password_target) as mock_password:
            assert sut._verify_password("", "") == False
            assert caplog.messages[0] == "No email or token provided."

    # Ensure the token/password verification function were not called.
    mock_token.assert_not_called()
    mock_password.assert_not_called()


def test_verify_password_auth_token(caplog):
    """
    :GIVEN: An auth token.
    :WHEN:  Verifying a users credentials.
    :THEN:  Verify the token authentication procedure is called.
    """
    # Target paths of functions to mock.
    auth_token_target = "app.api.authentication.auth_with_token"
    auth_password_target = "app.api.authentication.auth_with_password"

    token = "pytest_token"

    with patch(auth_token_target, return_value=False) as mock_token:
        with patch(auth_password_target, return_value=False) as mock_password:
            assert sut._verify_password(token, "") == False
            assert caplog.messages[0] == "Authorized with Token."

    # Assert token auth was called.
    mock_token.assert_called_once_with(token=token)
    mock_password.assert_not_called()


def test_verify_password_auth_password(caplog):
    """
    :GIVEN: An email and password.
    :WHEN:  Verifying a users credentials.
    :THEN:  Verify the password authentication procedure is called.
    """
    # Target paths of functions to mock.
    auth_token_target = "app.api.authentication.auth_with_token"
    auth_password_target = "app.api.authentication.auth_with_password"

    email = "pytest@example.com"
    password = "123abd"

    with patch(auth_token_target, return_value=False) as mock_token:
        with patch(auth_password_target, return_value=False) as mock_password:
            assert sut._verify_password(email, password) == False
            assert caplog.messages[0] == "Authorized with Email/Password."

    mock_token.assert_not_called()
    # Assert password auth was called.
    mock_password.assert_called_once_with(email=email, password=password)


def test_auth_with_password(mock_user_class_for):
    mock_user_class_for(sut)
    sut.auth_with_password("", "")
    assert False
