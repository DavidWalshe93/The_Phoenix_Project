"""
Author:     David Walshe
Date:       14 May 2021
"""

import json

from flask import Response

from tests.functional.utils import FlaskTestRig, basic_auth_header_field


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

    # Make request and gather response.
    res: Response = rig.client.post("/api/v1/login",
                                    headers=basic_auth_header_field(current_user["email"], current_user["password"]),
                                    data=current_user)

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify token was returned to client.
    assert data.get("token") != None
    # Assert status code was 200
    assert res.status_code == 200
