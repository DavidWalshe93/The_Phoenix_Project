"""
Author:     David Walshe
Date:       15 May 2021
"""

import json
from copy import deepcopy

import pytest
from flask import Response

from tests.functional.utils import FlaskTestRig, login, token_auth_header_field


@FlaskTestRig.setup_app(n_users=3)
def test_delete_me_no_auth_401(client_factory, make_users, **kwargs):
    """
    Validate an Unauthorised error is returned when attempting to delete
    the current user.

    :endpoint:  /api/v1/users/me
    :method:    DELETE
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
def test_delete_me_with_auth_user_200(client_factory, make_users, **kwargs):
    """
    Validate the current user can close their account.

    :endpoint:  /api/v1/users/me
    :method:    DELETE
    :auth:      True (Token)
    :params:    None
    :status:    200
    :response:  A list of user objects.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = [{"username": "tinybear433", "id": 0}]

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.delete("/api/v1/users/me", headers=token_auth_header_field(token))

    # Verify response matches expected.
    assert json.loads(res.data) == expected
    assert res.status_code == 200

    login(rig.client, user, should_fail=True)


@FlaskTestRig.setup_app(n_users=3)
def test_delete_users_with_auth_user_401(client_factory, make_users, **kwargs):
    """
    Validate a User role cannot bulk delete.

    :endpoint:  /api/v1/users
    :method:    DELETE
    :auth:      True (Token)
    :params:    None
    :status:    401
    :response:  401 error and message.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = {
        'error': 'Unauthorised',
        'message': 'Invalid credentials.'
    }

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.delete("/api/v1/users", headers=token_auth_header_field(token))

    # Verify response matches expected.
    assert json.loads(res.data) == expected
    assert res.status_code == 401


@FlaskTestRig.setup_app(n_users=10)
def test_delete_users_with_auth_admin_200(client_factory, make_users, **kwargs):
    """
    Validate a Admin role can bulk delete.

    :endpoint:  /api/v1/users
    :method:    DELETE
    :auth:      True (Token)
    :params:    None
    :status:    200
    :response:  id and username of deleted users.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    users_to_delete = {
        "users": [
            {"id": 0},
            {"id": 2}
        ]
    }

    expected = rig.get_current_users(keep_email=True, keep_password=True)
    expected = [expected[0], expected[2]]
    expected_full = deepcopy(expected)
    _ = [item.pop("last_login") for item in expected]
    _ = [item.pop("email") for item in expected]
    _ = [item.pop("password") for item in expected]

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True, admin_only=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.delete("/api/v1/users",
                                      headers=token_auth_header_field(token),
                                      data=json.dumps(users_to_delete))

    # Verify response matches expected.
    assert json.loads(res.data) == expected
    assert res.status_code == 200

    for user in expected_full:
        login(rig.client, user, should_fail=True)


@FlaskTestRig.setup_app(n_users=10)
@pytest.mark.parametrize("user_id", [3, 4, 5, 6, 7])
def test_delete_user_id_with_auth_admin_200(user_id, client_factory, make_users, **kwargs):
    """
    Validate a User role cannot bulk delete.

    :endpoint:  /api/v1/users
    :method:    DELETE
    :auth:      True (Token)
    :params:    None
    :status:    200
    :response:  The username and id of the deleted user.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = rig.get_current_users(keep_email=True, keep_password=True)[user_id]
    expected_full = deepcopy(expected)
    _ = [expected.pop(item) for item in ["email", "last_login", "password"]]

    print(expected)

    # Acquire login token for first user.
    user = rig.get_first_user(keep_password=True, admin_only=True)
    token = login(rig.client, user)

    # Make request and gather response.
    res: Response = rig.client.delete(f"/api/v1/users/{user_id}",
                                      headers=token_auth_header_field(token))

    # Verify response matches expected.
    assert json.loads(res.data) == [expected]
    assert res.status_code == 200

    login(rig.client, expected_full, should_fail=True)
