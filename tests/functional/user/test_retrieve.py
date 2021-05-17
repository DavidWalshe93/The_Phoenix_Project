"""
Author:     David Walshe
Date:       15 May 2021
"""

import json

import pytest
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
    res: Response = rig.client.get("/api/v1/users/me")

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 401


@FlaskTestRig.setup_app(n_users=3)
def test_get_user_me_with_auth_user(client_factory, make_users, **kwargs):
    """
    Validate the current user's information is returned on a
    GET request to /users endpoint.

    :endpoint:  /api/v1/user/me
    :method:    GET
    :auth:      True
    :params:    Auth Token
    :status:    200
    :response:  A object describing the current user.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = rig.get_first_user()

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get("/api/v1/users/me", headers=token_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)

    # Add the last_login field to the expected data.
    expected = [{**user, "last_login": datetime_as_string(user["last_login"])} for user in [expected]][0]

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200


@FlaskTestRig.setup_app(n_users=4)
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user_with_id_with_auth_user(user_id, client_factory, make_users, **kwargs):
    """
    Validate the current user's information is returned on a
    GET request to /users endpoint as a User.

    :endpoint:  /api/v1/user/<int:id>
    :method:    GET
    :auth:      True
    :params:    Auth Token, A user ID to get information on.
    :status:    200
    :response:  A object describing a user given the user's id,
                including the id, username and last_login time.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    # The expected user information to be returned.
    expected = rig.get_current_users(keep_email=False)[user_id]

    print(expected)

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get(f"/api/v1/users/{user_id}", headers=token_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)

    # Add the last_login field to the expected data.
    expected = [{**user, "last_login": datetime_as_string(user["last_login"])} for user in [expected]][0]

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200


@FlaskTestRig.setup_app(n_users=3)
def test_get_user_with_id_with_auth_user_404(client_factory, make_users, **kwargs):
    """
    Validate that a 404 error is raised when a non-existing id is queried
    against the database as a User.

    :endpoint:  /api/v1/user/<int:id>
    :method:    GET
    :auth:      True
    :params:    Auth Token, A user ID to get information on.
    :status:    404
    :response:  404 error due to user not existing.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    user_id = 100

    expected = {'error': 'Not Found', 'message': 'User does not exist.'}

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get(f"/api/v1/users/{user_id}", headers=token_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 404


@FlaskTestRig.setup_app(n_users=4)
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_users_with_auth_admin(user_id, client_factory, make_users, **kwargs):
    """
    Validate the a user keyed by their ID is returned on a
    GET request to /users endpoint as an Admin.

    :endpoint:  /api/v1/user/<int:id>
    :method:    GET
    :auth:      True
    :params:    Auth Token, A user ID to get information on.
    :status:    200
    :response:  A object describing a user given the user's id,
                including the id, username and last_login time.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    # The expected user information to be returned.
    expected = rig.get_current_users(keep_email=True, keep_role_name=user_id)[user_id]

    print(expected)

    # Acquire login token for first user.
    user = rig.get_first_user(keep_email=True, admin_only=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get(f"/api/v1/users/{user_id}", headers=token_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)

    # Add the last_login field to the expected data.
    expected = [{**user, "last_login": datetime_as_string(user["last_login"])} for user in [expected]][0]

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200


@FlaskTestRig.setup_app(n_users=3)
def test_get_user_with_id_with_auth_admin_404(client_factory, make_users, **kwargs):
    """
    Validate that a 404 error is raised when a non-existing id is queried
    against the database as a Admin.

    :endpoint:  /api/v1/user/<int:id>
    :method:    GET
    :auth:      True
    :params:    Auth Token, A user ID to get information on.
    :status:    404
    :response:  404 error due to user not existing.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    user_id = 100

    expected = {'error': 'Not Found', 'message': 'User does not exist.'}

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True, admin_only=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.get(f"/api/v1/users/{user_id}", headers=token_auth_header_token(token))

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 404
