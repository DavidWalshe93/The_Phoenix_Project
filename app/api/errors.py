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
    return jsonify({
        "error": error,
        "message": msg,
    })


def bad_request(msg: str) -> Response:
    """
    Creates and returns an error response for a 400 - Bad Request error.

    :param msg: The message to include in the error.
    :return: The 400 Error Response.
    """
    res = make_error(msg, "Bad Request")
    res.status_code = 400

    return res


def unauthorized(msg: str) -> Response:
    """
    Creates and returns an error response for a 401 - Unauthorised error.

    :param msg: The message to include in the error.
    :return: The 401 Error Response.
    """
    res = make_error(msg, "Unauthorised")
    res.status_code = 401

    return res


def not_found(msg: str) -> Response:
    """
    Creates and returns an error response for a 404 - Not Found error.

    :param msg: The message to include in the error.
    :return: The 404 Error Response.
    """
    res = make_error(msg, "Not Found")
    res.status_code = 404

    return res


def internal_server_error(msg: str) -> Response:
    """
    Creates and returns an error response for a 500 - Internal Server Error error.

    :param msg: The message to include in the error.
    :return: The 500 Error Response.
    """
    res = make_error(msg, "Internal Server Error")
    res.status_code = 500

    return res
