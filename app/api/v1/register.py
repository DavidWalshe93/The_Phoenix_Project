"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import current_app, make_response, request
from flask_restful import Resource
from flask_login import login_user

from app import db
from app.models.user import User
from app.api.errors import bad_request
from app.api.utils import create_request_parser, UserUtils

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

        pprint(request.data)

        parser = create_request_parser("name", "email", "password")

        # Get request JSON body (as bytes)
        req_json = parser.parse_args()

        pprint(req_json)

        # Create new User object from request body to check Database against.
        new_user: User = UserUtils.create_user_from(req_json)

        # User already exists, return a 400 error.
        if new_user.already_exists:
            logger.error("Registration error.")
            # Send back ambiguous message for security.
            return bad_request("Registration failed.")

        # Add new user to database.
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        logger.info(f"New user created.")
        expiry = current_app.config["TOKEN_EXPIRY"]
        return make_response(new_user.generate_auth_token(expiry), 201)
