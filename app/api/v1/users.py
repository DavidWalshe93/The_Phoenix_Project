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
        if id:
            # Query for a single user.
            results = User.query.get(id)
            many = False
        else:
            # Query database for all Users.
            results = User.query.all()
            many = True

        if not results:
            return not_found("User does not exist.")

        # Get currently authenticated user.
        user = auth.current_user()

        if user.is_admin:
            data = UserSchema(only=("id", "email", "username", "role_name", "last_login"), many=many).jsonify(results)
        else:
            data = UserSchema(only=("id", "username", "last_login"), many=many).jsonify(results)

        return make_response(data, 200)

    def put(self, id: int):
        # Get all users for deletion that are currently in DB.
        user = User.query.filter_by(id=id).first()

        if not user:
            return not_found("User does not exist.")

        data = UserSchema(only=("username", "password", "role_id")).parse_request()
        if data is None:
            return bad_request("Malformed request data.")

        update = False

        # Update username and/or password.
        for key in ["username", "password", "role_id"]:
            if data.get(key) is not None:
                logger.debug(f"{key} - Updated.")
                setattr(user, key, data.get(key))
                update = True

        # If the request didn't contain any updatable fields, send back error.
        if not update:
            return bad_request("Bad request data - Only 'username', 'password' and 'role_id' user fields can be updated.")

        # Commit changes to database
        db.session.add(user)
        db.session.commit()

        return make_response("Hello", 200)

    @staticmethod
    @auth.login_required(role=Access.ALL())
    def delete(id: int = None):
        """
        Deletes one or more users from the database.

        :return 200: All users were deleted successfully, returns a list of (id, username) for deleted entries.
        :return 401: Authentication failed.
        """
        return DeleteHandler(id=id).handle()





