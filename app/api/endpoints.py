"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging

from flask import jsonify, make_response
from flask_restful import Resource
from flask_login import login_required

from app.api.utils import UserInfo
from app.models.user import User

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

    def get(self):
        """
        Gathers all users in the given database and returns them as the response.

        :return: A JSON list of User objects.
        """
        # Query database for Users.
        results = User.query.with_entities(User.name, User.email, User.last_login).all()

        # Unpack result Row objects into UserInfo objects for response.
        data = [UserInfo.get(row) for row in results]

        return make_response(jsonify(data), 200)


class LoginAPI(Resource):

    def post(self):
        """
        Gathers all users in the given database and returns them as the response.

        :return: A JSON list of User objects.
        """
        pass




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
