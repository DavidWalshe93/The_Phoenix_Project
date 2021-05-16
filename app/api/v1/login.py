"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import current_app, make_response, request
from flask_restful import Resource

from app.models.user import User
from app.api.errors import bad_request
from app.api.v1.schema import UserSchema

logger = logging.getLogger(__name__)


class LoginApiV1(Resource):

    @staticmethod
    def post():
        """
        Logs in a user and returns a authentication token.

        :return 200: User sign-in successful, return Auth token.
        :return 400: User sign-in failure, account doesnt exist.
        """
        # Unpack request.
        data = UserSchema(only=("email", "password")).parse_request(as_ns=True)

        # Create new User object from request body to check Database against.
        current_user = User.query.filter_by(email=data.email).first()

        # User does not exist, return a 400 error.
        if not current_user or not current_user.already_exists:
            logger.error("Bad Request - User does not have an account.")
            return bad_request("Account does not exist, try registering instead.")

        logger.info(f"User {current_user.id} logged in.")

        return make_response(current_user.generate_auth_token(), 200)
