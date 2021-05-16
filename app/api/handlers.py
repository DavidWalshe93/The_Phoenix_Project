"""
Author:     David Walshe
Date:       16 May 2021
"""

import logging
from abc import abstractmethod

from app import db
from app.models.user import User
from app.api.utils import UserUtils, parse_request
from app.api.authentication import auth, Access
from app.api.errors import bad_request, not_found, unauthorized
from app.api.v1.schema import UserSchema, ValidationError

logger = logging.getLogger(__name__)


class Handler:

    def __init__(self, id: int):
        """
        Base handler class.

        Processes both user and admin roles.

        :param id: A user id.
        """
        self.id = id

    def handle(self):
        """
        External interface method to handle both users types, User and Admin accounts.

        Routing to correct role functionality is done internally.
        """
        # USER ROLE
        if self.id == "me":
            return self.handle_user()

        # ADMIN ROLE
        else:
            return self.handle_admin()

    @abstractmethod
    def handle_admin(self):
        pass

    @abstractmethod
    def handler_user(self):
        pass


