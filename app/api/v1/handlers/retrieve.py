"""
Author:     David Walshe
Date:       16 May 2021
"""

import logging
from typing import Union, List, Dict, Any

from flask import make_response, request

from app import db
from app.models.user import User
from app.api.authentication import auth, Access
from app.api.errors import bad_request, not_found
from app.api.v1.schema import UserSchema, ValidationError
from app.api.v1.handlers.base import Handler

logger = logging.getLogger(__name__)


class RetrieveHandler(Handler):

    def __init__(self, id: int):
        """
        Handles requests for User GET resources.

        :param id: ID of an individual user to return.
        """
        super().__init__(id)
        self.many = False

    @auth.login_required(role=Access.ALL())
    def handle(self):
        """
        Primary handler method to handle requests.

        :return: A list of users.
        """
        # Request for own data.
        if self.id == "me":
            return self.handle_me()

        # Get current logged in user.
        user = auth.current_user()

        # Get the requested user(s) objects.
        users = self.get_users()

        # Return 404 if user not found using /#
        if users is None:
            return not_found("User does not exist.")

        if user.is_admin:
            return self.handle_admin(users)
        else:
            return self.handle_user(users)

    @auth.login_required(role=Access.ADMIN_ONLY())
    def handle_admin(self, users):
        """
        Handles ADMIN role requests.

        :param users: The users to gather data on.
        :return: User data.
        """
        # Gather only certain data to return.
        data = UserSchema(only=("id", "email", "username", "role_name", "last_login"), many=self.many).jsonify(users)

        return make_response(data, 200)

    def handle_user(self, users):
        """
        Handles USER role requests.

        :param users: The users to gather data on.
        :return: User data.
        """
        data = UserSchema(only=("id", "username", "last_login"), many=self.many).jsonify(users)

        return make_response(data, 200)

    @staticmethod
    def handle_me():
        """
        Handles the common /me endpoint for both ADMIN and USER roles.

        :return: Returns data on the current signed in User.
        """
        # Get current User object.
        user = auth.current_user()

        # Convert the current User object into json.
        data = UserSchema(only=("id", "username", "email", "last_login",)).jsonify(user)

        return make_response(data, 200)

    def get_users(self):
        """
        Helper method to get User object(s) depending on if an id
        is passed or not.

        :return: A list or a single user.
        """
        if self.id:
            return self.get_single_user()
        else:
            return self.get_all_users()

    def get_single_user(self):
        """
        Returns a single user object keyed on the id requested.

        Returns None if ID does not match a DB row.

        :return: A User object or None.
        """
        # Query for a single user.
        return User.query.get(self.id)

    def get_all_users(self):
        """
        Gathers all users in the Database.

        :return: A list of all users in the Database.
        """
        self.many = True
        return User.query.all()
