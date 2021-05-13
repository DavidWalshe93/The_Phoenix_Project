"""
Author:     David Walshe
Date:       11 May 2021
"""

import pytest
import json

from flask import Response

from .utils import FlaskTestRig


# ======================================================================================================================
# Test helper functions.
# ======================================================================================================================

def assert_initial_state(rig, user_data):
    """
    Assert the initial state of the database to ensure the new user does not exist before creation request.

    :param rig: The flask test rig object.
    :param user_data: The user data to check for.
    :raises AssertionError: If user already exists in database.
    """
    with rig.app_context():
        user = rig.User.query.filter_by(email=user_data.get("email")).first()

        assert user == None


# ======================================================================================================================
# Endpoint tests
# ======================================================================================================================


@pytest.mark.parametrize("size", [0, 1, 3])
def test_get_users(size, client_factory, users):
    """
    Validate a list of all users is returned on a GET request to /users endpoint.

    :endpoint:  ~/v1/user
    :method:    GET
    :params:    None
    :status:    200
    :response:  A list of user objects.
    """
    expected = users(size=size, datetime_as_string=True)

    rig = FlaskTestRig.create(client_factory(size=size))

    # Make request and gather response.
    res: Response = rig.client.get("/v1/users")

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200


@pytest.mark.parametrize("size", [0, 1, 2, 3])
def test_create_user(size, client_factory, users, crypt, user_model):
    """
    Validate a user is created with a POST to ~/v1/user.

    :endpoint:  ~/v1/user
    :method:    POST
    :body:      New user information to add.
    :status:    201
    :response:  None
    """
    rig = FlaskTestRig.create(client_factory(size=size))

    # Test data
    user_data = {
        "name": "Susan Scot",
        "email": "Susan_Scot@example.com",
        "password": "tocS nasuS"
    }
    data = json.dumps(user_data)

    assert_initial_state(rig, user_data)

    # Make request and gather response.
    res: Response = rig.client.post("/v1/user", data=data)

    with rig.app_context():
        print(rig.User.query.all())
        # Assert a model entry has been created.
        user = rig.User.query.filter_by(email=user_data["email"]).first()

    assert type(user) == user_model

    # Verify response matches expected.
    assert user.name == user_data.get("name")
    assert user.email == user_data.get("email")
    # Test passwords have been hashed.
    assert user.password != user_data.get("password")
    assert len(user.password) == 60

    assert res.status_code == 201