"""
Author:     David Walshe
Date:       14 May 2021
"""

import json

from flask import Response

from tests.functional.utils import FlaskTestRig, basic_auth_header_token, datetime_as_string


@FlaskTestRig.setup_app(n_users=3)
def test_login_pass(client_factory, make_users, **kwargs):
    """
    Test successful login operation for existing user using a email/password.

    :endpoint:  /api/v1/user/register
    :method:    POST
    :auth:      False
    :params:    A current user's email/password.
    :status:    200
    :response:  A new authentication token.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    # Selected user for login attempt.
    current_user = rig.get_first_user(keep_password=True)

    print(current_user)

    # Make request and gather response.
    res: Response = rig.client.post("/api/v1/login", data=current_user)

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify token was returned to client.
    assert data.get("token") != None
    # Assert status code was 200
    assert res.status_code == 200

# def test_login_pass(client_factory, make_users):
#     """
#     Test successful login operation for existing user.
#
#     :endpoint:  /api/v1/user/register
#     :method:    POST
#     :auth:      False
#     :params:    A current user's email/password.
#     :status:    200
#     :response:  A new authentication token.
#     """
#     # Adds 3 users to the database.
#     existing_users = make_users(3, exclude_password=False)
#
#     rig = FlaskTestRig.create(client_factory(existing_users))
#
#     # Selected user for login attempt.
#     non_existing_user = make_users(1, exclude_password=False)
#
#     # Make request and gather response.
#     res: Response = rig.client.post("/api/v1/user/login", data=non_existing_user)
#
#     # Get JSON data returned.
#     data = json.loads(res.data)
#
#     # Verify token was returned to client.
#     assert data.get("token") != None
#     # Assert status code was 200
#     assert res.status_code == 200
