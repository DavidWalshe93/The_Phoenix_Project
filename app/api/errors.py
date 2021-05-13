"""
Author:     David Walshe
Date:       13 May 2021
"""

import logging

from flask import jsonify, Response

logger = logging.getLogger(__name__)


def make_error(msg: str, error: str) -> Response:
    """
    Creates and populates a Flask error response object.

    :param msg: The message to include in the error.
    :param error: The text description of the error.
    :return: A flask error response object.
    """
    response: Response = jsonify({
        "error": error,
        "message": msg,
    })


def unauthorized(msg: str) -> Response:
    """
    Creates and returns an error response for a 401 - Unauthorised error.

    :param msg: The message to include in the error.
    :return: The 401 Error Response.
    """
    res = make_error(msg, "unauthorised")
    res.status_code = 401

    return res
