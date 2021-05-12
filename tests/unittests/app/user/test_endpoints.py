"""
Author:     David Walshe
Date:       11 May 2021
"""

import pytest
import json

from flask import Response


@pytest.mark.parametrize("size", [1, 2, 3])
def test_get_users(size, client_factory, users):
    """
    Validate a list of all users is returned on a GET request to /users endpoint.

    :endpoint:  ~/v1/user
    :method:    GET
    :params:    None
    :response:  A list of user objects.
    """
    expected = users(size=size, datetime_as_string=True)

    client = client_factory(size=size)
    # Make request and gather response.
    res: Response = client.get("/v1/users")

    # Get JSON data returned.
    data = json.loads(res.data)

    # Verify response matches expected.
    assert data == expected
    assert res.status_code == 200
