"""
Author:     David Walshe
Date:       14 May 2021
"""
import json
import logging

from flask import jsonify, make_response, request
from flask_restful import Resource

from app import db
from app.models.user import User
from app.api.utils import UserUtils, parse_request
from app.api.authentication import auth, Access
from app.api.errors import bad_request
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
        # Query database for Users.
        results = User.query.all()

        # Get currently authenticated user.
        user = auth.current_user()

        if user.is_admin:
            logger.debug(f"Getting all users - as admin.")
            data = UserSchema(only=("id", "email", "username", "role_name", "last_login"), many=True).jsonify(results)
        else:
            logger.debug(f"Getting all users - as user.")
            data = UserSchema(only=("id", "username", "last_login"), many=True).jsonify(results)

        return make_response(data, 200)

    @staticmethod
    @auth.login_required(role=Access.ADMIN_ONLY())
    def delete(id: int = None):
        """
        Deletes one or more users from the database.

        :return 204: All users were deleted successfully.
        :return 401: Authentication failed.
        """
        try:
            users = UserSchema.parse_request(request, index="users", many=True, only=("id",))
        except ValidationError as err:
            msg = UserSchema.parse_validation_error(err)
            return bad_request(msg)

        ids = [user["id"] for user in users]

        # Delete all users passed.
        db.session.query(User).where(User.id.in_(ids)).delete()

        db.session.commit()

        return make_response({}, 204)
