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


class UpdateHandler(Handler):

    @auth.login_required(role=Access.ADMIN_ONLY())
    def handle_admin(self):
        """
        Handles administrator role updates.
        """
        # Get the user to update.
        user = User.query.filter_by(id=self.id).first()

        if not user:
            return not_found("User does not exist.")

        return self.update(user, only=("username", "password", "role_id"))

    @auth.login_required(role=Access.ALL())
    def handle_user(self):
        """
        Handles user role updates
        """
        user: User = auth.current_user()

        return self.update(user, only=("username", "password"))

    @staticmethod
    def update(user: User, only: tuple):
        """
        Updates a user in the database.

        :param user: The user to be updated.
        :param only: The fields that can be altered by the update.
        :return: No data is returned.
        """
        data = UserSchema(only=only).parse_request()

        if data is None:
            return bad_request("Malformed request data.")

        update = False

        # Update username and/or password.
        for key in only:
            if data.get(key) is not None:
                logger.debug(f"{key} - Updated.")
                setattr(user, key, data.get(key))
                update = True

        # If the request didn't contain any updatable fields, send back error.
        if not update:
            return bad_request(f"Bad request data - Only {only} user fields can be updated.")

        # Commit changes to database
        db.session.add(user)
        db.session.commit()

        return make_response({}, 200)
