"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging
from typing import Dict
from dataclasses import dataclass, asdict
from datetime import datetime
import json

from flask import jsonify, request
from sqlalchemy.engine.row import Row

from . import user
from .. import db
from ..models.user import User

logger = logging.getLogger(__name__)


@dataclass
class UserInfo:
    """
    Dataclass to convert User table Rows into an object mapping.
    """
    name: str
    email: str
    password: str
    last_login: datetime

    @staticmethod
    def get(row: Row):
        """
        Factory method to create a UserInfo object from a User database row.

        :param row: A row from the users table.
        :return: A UserInfo object with values extracted from the passed row.
        """
        return dict(name=row.name,
                    email=row.email,
                    last_login=row.last_login)

    @classmethod
    def create(cls, data: bytes) -> Dict:
        """
        Factory method to create a UserInfo object with passwords hashed.

        :param data: The json data passed from a POST request.
        :return: A UserInfo object describing the new user.
        """
        # Convert to JSON if of type bytes.
        if type(data) == bytes:
            data = json.loads(data)

        return asdict(cls(
            name=data.get("name", None),
            email=data.get("email", None),
            password=data.get("password", None),
            last_login=datetime.now()
        ))


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
