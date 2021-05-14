"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import jsonify, make_response
from flask_login import login_required
from flask_restful import Resource

from app.models.user import User
from app.api.utils import UserUtils
from app.api.authentication import auth

logger = logging.getLogger(__name__)


class UsersApiV1(Resource):

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
