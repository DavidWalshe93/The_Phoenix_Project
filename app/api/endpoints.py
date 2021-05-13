"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging
from dataclasses import dataclass

from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_login import login_required, login_user

from .. import db
from ..api.utils import UserUtils
from ..models.user import User
from .authentication import auth
from .errors import bad_request

logger = logging.getLogger(__name__)


class UserAPI(Resource):

    def get(self):
        pass

    @login_required
    def put(self):
        pass

    def delete(self):
        pass


class UsersAPI(Resource):

    @auth.login_required
    def get(self):
        """
        Gathers all users in the given database and returns them as the response.

        :return: A JSON list of User objects.
        """
        # Query database for Users.
        results = User.query.with_entities(User.name, User.email, User.last_login).all()

        # Unpack result Row objects into UserInfo objects for response.
        data = [UserUtils.dict_from_user_row(row) for row in results]

        return make_response(jsonify(data), 200)


register_parser = reqparse.RequestParser()
register_parser.add_argument("name")
register_parser.add_argument("email")
register_parser.add_argument("password")


class RegisterAPI(Resource):

    def post(self):
        """
        Creates a user object in the database and returns an authentication token to the client.

        :return 201: User registration successful, user added to DB, return Auth token.
        :return 400: User registration failure - email already in use.
        """
        # Get request JSON body (as bytes)
        req_json = register_parser.parse_args()

        # Create new User object from request body to check Database against.
        new_user: User = UserUtils.create_user_from(req_json)

        # User already exists, return a 400 error.
        if new_user.already_exists:
            logger.error(f"Bad Request - Duplicate email when trying to register.")
            return bad_request("Email already exists. Try logging in instead.")

        # Add new user to database.
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        logger.info(f"New user created.")
        return make_response(new_user.generate_auth_token(3600), 201)


login_parser = reqparse.RequestParser()
login_parser.add_argument("email")
login_parser.add_argument("password")


class LoginAPI(Resource):

    def post(self):
        """
        Logs in a user and returns a authentication token.

        :return 200: User sign-in successful, return Auth token.
        :return 400: User sign-in failure, account doesnt exist.
        """
        # Get request JSON body (as bytes)
        req_json = register_parser.parse_args()

        # Create new User object from request body to check Database against.
        current_user = User.query.filter_by(email=req_json.email).first()

        # User does not exist, return a 400 error.
        if not current_user or not current_user.already_exists:
            logger.error(f"Bad Request - User does not have an account.")
            return bad_request("Account does not exist, try registering instead.")

        login_user(current_user)

        logger.info(f"User {current_user.id} logged in.")
        return make_response(current_user.generate_auth_token(3600), 200)

# @user.route("/api/v1/user", methods=["POST"])
# def register():
#     """
#     Creates a user object in the database.
#
#     :return: A 201 response.
#     """
#     # Get request JSON body (as bytes)
#     req_json = request.get_data()
#
#     # Use factory to create new user information dictionary.
#     user_info: dict = UserInfo.create(req_json)
#
#     # Create new user object.
#     new_user = User(**user_info)
#
#     # Add new user to database.
#     db.session.add(new_user)
#     db.session.commit()
#
#     login_user(new_user)
#
#     return "", 201

# @user.route("/v1/users", methods=["GET"])
# @login_required
# def get_users():
#     """
#     Gathers all users in the given database and returns them as the response.
#
#     :return: A json list of User objects.
#     """
#     # Query database for Users.
#     results = User.query.with_entities(User.name, User.email, User.last_login).all()
#
#     # Unpack result Row objects into UserInfo objects for response.
#     data = [UserInfo.get(row) for row in results]
#
#     return jsonify(data)
