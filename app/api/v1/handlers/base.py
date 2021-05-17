"""
Author:     David Walshe
Date:       16 May 2021
"""

import logging
from abc import abstractmethod

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
    def handle_user(self):
        pass
