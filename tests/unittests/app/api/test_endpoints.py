"""
Author:     David Walshe
Date:       11 May 2021
"""

import json

from flask import Response

from tests.functional.utils import FlaskTestRig

NUM_USERS = 3


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


def test_register(client_factory):
    """
    Validate a user is created with a POST to ~/v1/user.

    :endpoint:  ~/v1/user
    :method:    POST
    :body:      New user information to add.
    :status:    201
    :response:  None
    """
    rig = FlaskTestRig.create(client_factory(size=NUM_USERS))

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
        # Assert a model entry has been created.
        user = rig.User.query.filter_by(email=user_data["email"]).first()

    # Verify a user object was returned.
    assert isinstance(user, rig.User)

    # Verify response matches expected.
    assert user.name == user_data.get("name")
    assert user.email == user_data.get("email")
    # Test passwords have been hashed.
    assert user.password_hash != user_data.get("password")
    assert len(user.password_hash) == 94
    # Verify status code.
    assert res.status_code == 201
