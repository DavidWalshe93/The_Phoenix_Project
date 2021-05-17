"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask_restful import Resource

from app.api.utils import UserUtils
from app.api.authentication import auth, Access

from app.api.v1.handlers import UpdateHandler, RetrieveHandler, DeleteHandler

logger = logging.getLogger(__name__)


class UsersApiV1(Resource):

    @staticmethod
    @auth.login_required(role=Access.ALL())
    def get(id: int = None):
        """
        Gathers all users in the given database and returns them as the response.

        :return 200: A JSON list of User objects.
        :return 401: Authentication failed.
        """
        return RetrieveHandler(id).handle()

    @staticmethod
    def delete(id: int = None):
        """
        Deletes one or more users from the database.

        :return 200: All users were deleted successfully, returns a list of (id, username) for deleted entries.
        :return 401: Authentication failed.
        :return 404: User not found in database (Admin single user deletions only).
        """
        return DeleteHandler(id=id).handle()

    def put(self, id: int):
        """
        Deletes one or more users from the database.

        :return 200: User update was successful.
        :return 401: Authentication failed.
        :return 404: User not found in database (Admin single user updates only).
        """
        return UpdateHandler(id).handle()
