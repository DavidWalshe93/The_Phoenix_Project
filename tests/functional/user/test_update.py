"""
Author:     David Walshe
Date:       15 May 2021
"""

import pytest

import json

from flask import Response

from tests.functional.utils import FlaskTestRig, login, token_auth_header_token, datetime_as_string


@FlaskTestRig.setup_app(n_users=3)
def test_updated_user_me_no_auth(client_factory, make_users, **kwargs):
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
    res: Response = rig.client.put("/api/v1/users/me", data={"name": "foobar", "password": "top_secret"})

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 401


@FlaskTestRig.setup_app(n_users=3)
@pytest.mark.parametrize("req_data",
                         [
                             {"name": "foobar"},
                             {"password": "top_secret"},
                             {"name": "foobar", "password": "top_secret"}
                         ])
def test_updated_user_me_with_auth(req_data, client_factory, make_users, **kwargs):
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

    expected = rig.get_first_user()

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.put("/api/v1/users/me", headers=token_auth_header_token(token), data=req_data)

    # Verify response matches expected.
    assert res.data == b""
    assert res.status_code == 204
