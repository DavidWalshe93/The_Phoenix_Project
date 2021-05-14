"""
Author:     David Walshe
Date:       13 May 2021
"""

import pytest
import json

from flask import Response

from tests.functional.utils import FlaskTestRig, login, basic_auth_header_token, datetime_as_string

NUM_USERS = 3


def test_get_users_no_auth(client_factory):
    """
    Validate an Unauthorised error is returned when attempting to list of
    all users on a GET request to /api/v1/users endpoint without being
    authenticated.

    :endpoint:  /api/v1/users
    :method:    GET
    :auth:      False
    :params:    None
    :status:    401
    :response:  An unauthorised error.
    """
    expected = {
        "error": "Unauthorised",
        "message": "Invalid user credentials to access resource."
    }

    rig = FlaskTestRig.create(client_factory())

    # Make request and gather response.
    res: Response = rig.client.get("/api/v1/users")

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 401


def test_get_users_with_auth(client_factory, make_users):
    """
    Validate a list of all users is returned on a GET request to /users endpoint.

    :endpoint:  /api/v1/users
    :method:    GET
    :auth:      True
    :params:    None
    :status:    200
    :response:  A list of user objects.
    """
    expected = make_users(size=50)

    rig = FlaskTestRig.create(client_factory(expected))

    # Acquire login token for first user.
    user = expected[0]
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get("/api/v1/users", headers=basic_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)

    expected = [{**user, "last_login": datetime_as_string(user["last_login"])} for user in expected]

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200
