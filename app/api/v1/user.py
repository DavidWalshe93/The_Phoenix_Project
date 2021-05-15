"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import make_response
from flask_restful import Resource

from app import db
from app.models.user import User
from app.api.authentication import auth
from app.api.utils import create_request_parser
from app.api.errors import bad_request

logger = logging.getLogger(__name__)


class UserApiV1(Resource):

    @auth.login_required
    def get(self):
        """
        Returns the current user's information.

        :return 200: The current user's information.
        :return 401: Bad user credentials.
        """
        # Get current User object.
        user = auth.current_user()

        # Get user information.
        data = user.as_dict()
        # Remove id field.
        data.pop("id")

        return make_response(data, 200)

    @auth.login_required
    def put(self):
        """
        Updates a users username and/or password credentials.

        Updating the password credential will need re-authentication.

        :return 204: User was updated.
        :return 400: Bad request body, missing both username and/or password fields to update.
        :return 401: Bad user credentials.
        """
        # Get current User object.
        user: User = auth.current_user()

        # Get request data.
        parser = create_request_parser("username", "password")
        data = parser.parse_args()

        # Flag to check if any updates occured.
        update = False

        # Update username and/or password.
        for key in ["username", "password"]:
            if data.get(key) is not None:
                logger.debug(f"{key} - Updated.")
                setattr(user, key, data.get(key))
                update = True

        # If the request didn't contain any updatable fields, send back error.
        if not update:
            return bad_request("Bad request data - Only 'username' and 'password' user fields can be updated.")

        # Commit changes to database
        db.session.add(user)
        db.session.commit()

        return make_response({}, 204)

    @auth.login_required
    def delete(self):
        """
        Deletes the current user from the system.

        :return 204: User was updated.
        :return 401: Bad user credentials.
        """
        user: User = auth.current_user()

        db.session.delete(user)
        db.session.commit()

        return make_response({}, 204)
