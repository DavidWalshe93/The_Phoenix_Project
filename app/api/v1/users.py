"""
Author:     David Walshe
Date:       14 May 2021
"""
import json
import logging
from typing import Union, List, Dict, Any

from flask import jsonify, make_response, request
from flask_restful import Resource

from app import db
from app.models.user import User
from app.api.utils import UserUtils, parse_request
from app.api.authentication import auth, Access
from app.api.errors import bad_request, not_found, unauthorized
from app.api.v1.schema import UserSchema, ValidationError

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
        # if id:
        #     # Query for a single user.
        #     results = User.query.get(id)
        #     many = False
        # else:
        #     # Query database for all Users.
        #     results = User.query.all()
        #     many = True
        #
        # if not results:
        #     return not_found("User does not exist.")
        #
        # # Get currently authenticated user.
        # user = auth.current_user()
        #
        # if user.is_admin:
        #     data = UserSchema(only=("id", "email", "username", "role_name", "last_login"), many=many).jsonify(results)
        # else:
        #     data = UserSchema(only=("id", "username", "last_login"), many=many).jsonify(results)
        #
        # return make_response(data, 200)

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
