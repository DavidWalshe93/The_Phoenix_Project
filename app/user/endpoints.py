"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging
from typing import TYPE_CHECKING
from dataclasses import dataclass, asdict
from datetime import datetime

from flask import jsonify
from sqlalchemy.engine.row import Row

from . import user
from ..models.user import User

logger = logging.getLogger(__name__)


@dataclass
class UserInfo:
    """
    Dataclass to convert User table Rows into an object mapping.
    """
    name: str
    email: str
    last_login: datetime

    @classmethod
    def unpack(cls, row: Row):
        """
        Factory method to creact a UserInfo object from a User database row.

        :param row: A row from the users table.
        :return: A UserInfo object with values extracted from the passed row.
        """
        return cls(name=row.name,
                   email=row.email,
                   last_login=row.last_login)


@user.route("/v1/users", methods=["GET"])
def get_users():
    """
    Gathers all users in the given database and returns them as the response.

    :return: A json list of User objects.
    """
    # Query database for Users.
    results = User.query.with_entities(User.name, User.email, User.last_login).all()

    # Unpack result Row objects into UserInfo objects for response.
    data = [UserInfo.unpack(row) for row in results]

    return jsonify(data)
