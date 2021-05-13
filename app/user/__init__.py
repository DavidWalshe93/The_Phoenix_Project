"""
Author:     David Walshe
Date:       11 May 2021
"""

from flask import Blueprint

user = Blueprint("user", __name__)

from . import endpoints, errors

from .endpoints import UserAPI, UsersAPI
