"""
Author:     David Walshe
Date:       13 May 2021
"""

import os
import json

from flask import Response

from tests.functional.utils import FlaskTestRig


@FlaskTestRig.setup_app(n_users=3)
def test_register_pass(client_factory, make_users, **kwargs):
    """
    Test successful registration operation for new user.

    :endpoint:  /api/v1/user/register
    :method:    POST
    :auth:      False
    :params:    New user email/password.
    :status:    201
    :response:  A new authentication token.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    new_user = rig.create_new_user(keep_password=True, keep_role_id=True)

    new_user["admin_password"] = os.environ["ADMIN_SECRET_KEY"]

    # Make request and gather response.
    res: Response = rig.client.post("/api/v1/register", data=new_user)

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify token was returned to client.
    assert data.get("token") != None
    assert res.status_code == 201


@FlaskTestRig.setup_app(n_users=3)
def test_register_fail(client_factory, make_users, **kwargs):
    """
    Verifies an 400 error occurs if a current user tries to re-register an account.
    
    :endpoint:  /api/v1/user/register
    :method:    POST
    :auth:      False
    :params:    Email/Password/Username
    :status:    400
    :response:  An error message stating the user already has an account for the email used.
    """
    rig: FlaskTestRig = FlaskTestRig.extract_rig_from_kwargs(kwargs)

    expected = {
        "error": "Bad Request",
        "message": "Registration failed."
    }

    current_user = rig.get_first_user(keep_password=True)
    print(current_user)

    # Make request and gather response.
    res: Response = rig.client.post("/api/v1/register", data=current_user)

    # Get JSON data returned.
    data = json.loads(res.data)

    # Assert token is not returned to client.
    assert data.get("token") == None
    # Assert error msg content.
    assert data.get("error") == expected["error"]
    assert data.get("message") == expected["message"]
    # Assert error status code.
    assert res.status_code == 400
