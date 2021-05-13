"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging
import json

from flask import jsonify, request
from flask_login import login_required

from . import user
from .utils import UserInfo
from .. import db
from ..models.user import User

logger = logging.getLogger(__name__)


@user.route("/v1/users", methods=["GET"])
def get_users():
    """
    Gathers all users in the given database and returns them as the response.

    :return: A json list of User objects.
    """
    # Query database for Users.
    results = User.query.with_entities(User.name, User.email, User.last_login).all()

    # Unpack result Row objects into UserInfo objects for response.
    data = [UserInfo.get(row) for row in results]

    return jsonify(data)


@user.route("/v1/user", methods=["POST"])
def create_user():
    """
    Creates a user object in the database.

    :return: A 201 response.
    """
    # Get request JSON body (as bytes)
    req_json = request.get_data()

    # Use factory to create new user information dictionary.
    user_info = UserInfo.create(req_json)

    # Create new user object.
    new_user = User(**user_info)

    # Add new user to database.
    db.session.add(new_user)
    db.session.commit()

    return "", 201
