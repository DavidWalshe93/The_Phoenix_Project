"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import g, session, make_response
# from flask_login import login_required
from flask_restful import Resource

from app.api.authentication import auth
from app.models.user import User

logger = logging.getLogger(__name__)


class UserApiV1(Resource):

    @auth.login_required
    def get(self):
        """
        Returns the current users information.

        :return 200: The current user's information.
        :return 400: Bad user credentials.
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
        pass

    @auth.login_required
    def delete(self):
        pass
