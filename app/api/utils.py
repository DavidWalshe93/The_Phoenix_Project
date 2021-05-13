"""
Author:     David Walshe
Date:       13 May 2021
"""

import logging
from datetime import datetime
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any

from sqlalchemy.engine.row import Row

from ..models import User

logger = logging.getLogger(__name__)


@dataclass
class UserFactory:
    """
    Dataclass to convert User table Rows into an object mapping.
    """
    name: str
    email: str
    password: str
    last_login: datetime

    # @staticmethod
    # def get(row: Row) -> Dict[str, Any]:
    #     """
    #     Factory method to create a UserInfo object from a User database row.
    #
    #     :param row: A row from the users table.
    #     :return: A UserInfo object with values extracted from the passed row.
    #     """
    #     return dict(name=row.name,
    #                 email=row.email,
    #                 last_login=row.last_login)

    @classmethod
    def create_user_from(cls, data: bytes) -> User:
        """
        Factory method to create a User object for registration.

        :param data: The json data passed from a POST request.
        :return: A User object describing the new user.
        """
        # Convert to JSON if of type bytes.
        if isinstance(data, bytes):
            data = json.loads(data)

        return User(**asdict(cls(
            name=data.get("name", None),
            email=data.get("email", None),
            password=data.get("password", None),
            last_login=datetime.now()
        )))
