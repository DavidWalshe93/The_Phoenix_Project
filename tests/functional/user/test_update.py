"""
Author:     David Walshe
Date:       15 May 2021
"""

import json

import pytest
from flask import Response
from werkzeug.security import check_password_hash

from tests.functional.utils import FlaskTestRig, login, token_auth_header_token, datetime_as_string
from app.models import User


@FlaskTestRig.setup_app(n_users=3)
def test_updated_user_me_no_auth_401(client_factory, make_users, **kwargs):
    """
    Attempts to update the current user without authentication.

    :endpoint:  /api/v1/users/me
    :method:    PUT
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
def test_updated_user_me_with_auth_204(req_data, client_factory, make_users, **kwargs):
    """
    Updates the currently logged in user.

    :endpoint:  /api/v1/user/me
    :method:    PUT
    :auth:      True
    :params:    Auth Token, new name and/or password values for user.
    :status:    204
    :response:  Nothing.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.put("/api/v1/users/me", headers=token_auth_header_token(token), data=req_data)

    # Verify the updates on the database.
    with rig.app_context():
        actual: User = rig.User.user_from_email(user.get("email"))

    if req_data.get("password"):
        assert actual.verify_password(req_data["password"]) == True
    if req_data.get("name"):
        assert actual.name == req_data["name"]

    # Verify response matches expected.
    assert res.data == b""
    assert res.status_code == 204


@FlaskTestRig.setup_app(n_users=3)
def test_updated_user_me_with_auth_400(client_factory, make_users, **kwargs):
    """
    Attempts to update the current user but fails due to no update data being sent.

    :endpoint:  /api/v1/user/me
    :method:    PUT
    :auth:      True
    :params:    Auth Token
    :status:    400
    :response:  Bad request due to no 'name' or 'password' fields being included in the request.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = {
        "error": "Bad Request",
        "message": "Bad request data - Only 'name' and 'password' user fields can be updated."
    }

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.put("/api/v1/users/me", headers=token_auth_header_token(token), data={})

    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 400
