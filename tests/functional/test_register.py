"""
Author:     David Walshe
Date:       13 May 2021
"""

import pytest
import json

from flask import Response

from tests.functional.utils import FlaskTestRig, login, basic_auth_header_token, datetime_as_string


def test_register_pass(client_factory, make_users):
    """
    Test successful registration operation for new user.

    :endpoint:  /api/v1/user/register
    :method:    POST
    :auth:      False
    :params:    New user email/password.
    :status:    201
    :response:  A new authentication token.
    """
    existing_users = make_users(1, exclude_password=False)
    new_users = make_users(1, exclude_password=False)

    rig = FlaskTestRig.create(client_factory(existing_users))

    # Make request and gather response.
    res: Response = rig.client.post("/api/v1/user/register", data=new_users[0])

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify token was returned to client.
    assert data.get("token") != None
    assert res.status_code == 201


def test_register_fail(client_factory, make_users):
    """
    Verifies an 400 error occurs if a current user tries to re-register an account.
    
    :endpoint:  /api/v1/user/register
    :method:    POST
    :auth:      False
    :params:    Email/Password/Username
    :status:    400
    :response:  An error message stating the user already has an account for the email used.
    """
    expected = {
        "error": "Bad Request",
        "message": "Email already exists. Try logging in instead."
    }

    existing_users = make_users(1, exclude_password=False)

    rig = FlaskTestRig.create(client_factory(existing_users))

    # Make request and gather response.
    res: Response = rig.client.post("/api/v1/user/register", data=existing_users[0])

    # Get JSON data returned.
    data = json.loads(res.data)

    # Assert token is not returned to client.
    assert data.get("token") == None
    # Assert error msg content.
    assert data.get("error") == expected["error"]
    assert data.get("message") == expected["message"]
    # Assert error status code.
    assert res.status_code == 400
