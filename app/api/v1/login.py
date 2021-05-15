"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import current_app, make_response
from flask_restful import Resource
from flask_login import login_user

from app.models.user import User
from app.api.errors import bad_request
from app.api.utils import create_request_parser

logger = logging.getLogger(__name__)


class LoginApiV1(Resource):

    @staticmethod
    def post():
        """
        Logs in a user and returns a authentication token.

        :return 200: User sign-in successful, return Auth token.
        :return 400: User sign-in failure, account doesnt exist.
        """
        # Create a request parser
        parser = create_request_parser("email", "password")

        # Get request JSON body (as bytes)
        req_json = parser.parse_args()

        # Create new User object from request body to check Database against.
        current_user = User.query.filter_by(email=req_json.email).first()

        # User does not exist, return a 400 error.
        if not current_user or not current_user.already_exists:
            logger.error(f"Bad Request - User does not have an account.")
            return bad_request("Account does not exist, try registering instead.")

        login_user(current_user)

        logger.info(f"User {current_user.id} logged in.")

        expiry = current_app.config["TOKEN_EXPIRY"]
        return make_response(current_user.generate_auth_token(expiry), 200)
