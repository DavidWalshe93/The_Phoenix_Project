"""
Author:     David Walshe
Date:       15 May 2021
"""

import json

from flask import Response

from tests.functional.utils import FlaskTestRig, login, token_auth_header_token, datetime_as_string


@FlaskTestRig.setup_app(n_users=3)
def test_get_user_me_no_auth(client_factory, make_users, **kwargs):
    """
    Validate an Unauthorised error is returned when attempting to get
    a users information on a GET request to /api/v1/user/me endpoint without being
    authenticated.

    :endpoint:  /api/v1/users/me
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
    res: Response = rig.client.delete("/api/v1/users/me")

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 401


@FlaskTestRig.setup_app(n_users=3)
def test_get_user_me_with_auth(client_factory, make_users, **kwargs):
    """
    Validate the current user's information is returned on a
    GET request to /users endpoint.

    :endpoint:  /api/v1/user/me
    :method:    GET
    :auth:      True
    :params:    Auth Token
    :status:    200
    :response:  A list of user objects.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = [{"username": "tinybear433", "id": 0}]

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.delete("/api/v1/users/me", headers=token_auth_header_token(token))

    # Verify response matches expected.
    assert json.loads(res.data) == expected
    assert res.status_code == 200

    login(rig.client, user, should_fail=True)
