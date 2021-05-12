"""
Author:     David Walshe
Date:       11 May 2021
"""

import pytest
import json

from flask import Response


def test_get_users(client, users):
    """
    Validated a list of users is returned on a GET to /users endpoint.

    :endpoint:  ~/v1/user
    :method:    GET
    :params:    None
    :response:  A list of user objects.
    """
    expected = users(datetime_as_string=True)

    # Make request and gather response.
    res: Response = client.get("/v1/users")

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200
