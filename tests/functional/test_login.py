"""
Author:     David Walshe
Date:       14 May 2021
"""

import pytest
import json

from flask import Response

from tests.functional.utils import FlaskTestRig, login, basic_auth_header_token, datetime_as_string


def test_login_pass(client_factory, make_users):
    """
    Test successful login operation for existing user.

    :endpoint:  /api/v1/user/register
    :method:    POST
    :auth:      False
    :params:    A current user's email/password.
    :status:    200
    :response:  A new authentication token.
    """
    existing_users = make_users(3, exclude_password=False)

    rig = FlaskTestRig.create(client_factory(existing_users))

    # Selected user for login attempt.
    current_user = existing_users[0]

    # Make request and gather response.
    res: Response = rig.client.post("/api/v1/user/login", data=current_user)

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify token was returned to client.
    assert data.get("token") != None
    # Assert status code was 200
    assert res.status_code == 200
