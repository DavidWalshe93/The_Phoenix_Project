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
        super().__init__(id)
        self.many = False

    @auth.login_required(role=Access.ALL())
    def handle(self):

        if self.id == "me":
            return self.handle_me()

        user = auth.current_user()

        if user.is_admin:
            data = self.handle_admin()
        else:
            data = self.handle_user()

        return make_response(data, 200)

    @auth.login_required(role=Access.ADMIN_ONLY())
    def handle_admin(self):
        users = self.get_users()

        if users is None:
            return not_found("User does not exist.")

        return UserSchema(only=("id", "email", "username", "role_name", "last_login"), many=self.many).jsonify(users)

    def handle_user(self):
        users = self.get_users()

        if users is None:
            return not_found("User does not exist.")

        return UserSchema(only=("id", "username", "last_login"), many=self.many).jsonify(users)

    @staticmethod
    def handle_me():
        # Get current User object.
        user = auth.current_user()

        # Convert the current User object into json.
        data = UserSchema(only=("id", "username", "email", "last_login",)).jsonify(user)

        return make_response(data, 200)

    def get_users(self):
        if self.id:
            return self.get_single_user()
        else:
            return self.get_all_users()

    def get_single_user(self):
        # Query for a single user.
        return User.query.get(self.id)

    def get_all_users(self):
        self.many = True
        return User.query.all()
