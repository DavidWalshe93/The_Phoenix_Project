"""
Author:     David Walshe
Date:       14 May 2021
"""

import pytest
from dataclasses import dataclass
import json

from flask import Response

import app.api.errors as sut


@dataclass
class Expected:
    """An object to hold the expected test response."""
    message: str
    error: str
    status_code: int


@dataclass
class Actual:
    """An object to hold the actual test response."""
    message: str
    error: str
    status_code: int

    @classmethod
    def parse_response(cls, response: Response):
        """
        Parses data from a error Flask Response.

        :param response: The Response object to parse.
        :return: A Actual object.
        """
        data = json.loads(response.data)

        return cls(
            message=data["message"],
            error=data["error"],
            status_code=response.status_code
        )

    def __eq__(self, other: Expected) -> bool:
        """
        Checks for equality against an expected object.

        :param other: An expected object.
        :return: True if Actual == Expected, else False
        """
        return all([
            self.error == other.error,
            self.message == other.message,
            self.status_code == other.status_code
        ])


def test_bad_request(app_context):
    """
    :GIVEN: An error msg.
    :WHEN:  Generating a Bad Request error.
    :THEN:  Verify the Bad Request is created with the correct information.
    """
    expected = Expected(
        message="Hello Pytest",
        error="Bad Request",
        status_code=400
    )

    with app_context:
        actual = Actual.parse_response(sut.bad_request(expected.message))

    assert actual == expected


def test_unauthorized(app_context):
    """
    :GIVEN: An error msg.
    :WHEN:  Generating an Unauthorised error.
    :THEN:  Verify the Unauthorised is created with the correct information.
    """
    expected = Expected(
        message="Hello Pytest",
        error="Unauthorised",
        status_code=401
    )

    with app_context:
        actual = Actual.parse_response(sut.unauthorized(expected.message))

    assert actual == expected


def test_internal_server_error(app_context):
    """
    :GIVEN: An error msg.
    :WHEN:  Generating an Internal Server Error error.
    :THEN:  Verify the Internal Server Error is created with the correct information.
    """
    expected = Expected(
        message="Hello Pytest",
        error="Internal Server Error",
        status_code=500
    )

    with app_context:
        actual = Actual.parse_response(sut.internal_server_error(expected.message))

    assert actual == expected