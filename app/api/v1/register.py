"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import current_app, make_response, request
from flask_restful import Resource

from app import db
from app.models.user import User
from app.api.errors import bad_request
from app.api.utils import create_request_parser, UserUtils
from app.api.authentication import verify_admin_password

logger = logging.getLogger(__name__)


class RegisterApiV1(Resource):

    @staticmethod
    def post():
        """
        Creates a user object in the database and returns an authentication token to the client.

        :return 201: User registration successful, user added to DB, return Auth token.
        :return 400: User registration failure - email already in use.
        """
        from pprint import pprint

        parser = create_request_parser("username", "email", "password", "admin_password")

        # Get request JSON body (as bytes)
        req_json = parser.parse_args()

        # Check if user is an admin.
        is_admin = verify_admin_password(req_json.get("admin_password"))

        # Create new User object from request body to check Database against.
        new_user: User = UserUtils.create_user_from(req_json, is_admin=is_admin)

        # User already exists, return a 400 error.
        if new_user.already_exists:
            logger.error("Registration error.")
            # Send back ambiguous message for security.
            return bad_request("Registration failed.")

        # Add new user to database.
        db.session.add(new_user)
        db.session.commit()

        if is_admin:
            logger.info("New admin created.")
        else:
            logger.info("New user created.")

        expiry = current_app.config["TOKEN_EXPIRY"]
        return make_response(new_user.generate_auth_token(expiry), 201)
