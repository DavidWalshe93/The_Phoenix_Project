"""
Author:     David Walshe
Date:       13 May 2021
"""

import json

from flask import Response

from tests.functional.utils import FlaskTestRig, login, token_auth_header_token


@FlaskTestRig.setup_app(n_users=3)
def test_get_users_no_auth(client_factory, make_users, **kwargs):
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
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = {
        "error": "Unauthorised",
        "message": "Invalid credentials."
    }

    # Make request and gather response.
    res: Response = rig.client.get("/api/v1/users")

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 401


@FlaskTestRig.setup_app(n_users=3)
def test_get_users_with_auth_as_user(client_factory, make_users, **kwargs):
    """
    Validate a list of all users is returned on a GET request to /users endpoint.

    As a User role, only usernames and last-logins should be returned.

    :endpoint:  /api/v1/users
    :method:    GET
    :auth:      True
    :params:    Auth Token
    :status:    200
    :response:  A list of user objects containing username and last_login fields.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = rig.get_current_users(keep_email=False)
    _ = [item.pop("last_login") for item in expected]

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get("/api/v1/users", headers=token_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)
    _ = [item.pop("last_login") for item in data]

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200


@FlaskTestRig.setup_app(n_users=3)
def test_get_users_with_auth_as_admin(client_factory, make_users, **kwargs):
    """
    Validate a list of all users is returned on a GET request to /users endpoint.

    As a Admin role, emails, usernames and last-logins should be returned.

    :endpoint:  /api/v1/users
    :method:    GET
    :auth:      True
    :params:    Auth Token
    :status:    200
    :response:  A list of user objects containing email, username and last_login fields.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = rig.get_current_users(keep_role_name=True)
    _ = [item.pop("last_login") for item in expected]

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True, admin_only=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get("/api/v1/users", headers=token_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)
    _ = [item.pop("last_login") for item in data]

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200
