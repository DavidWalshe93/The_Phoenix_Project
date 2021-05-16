"""
Author:     David Walshe
Date:       13 May 2021
"""

from flask import Blueprint

from .v1 import LoginApiV1, RegisterApiV1, UsersApiV1


def get_blueprint():
    """API Blueprint factory."""
    return Blueprint("api", __name__)
