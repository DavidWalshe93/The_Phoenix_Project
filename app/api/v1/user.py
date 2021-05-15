"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import g, session
# from flask_login import login_required
from flask_restful import Resource

from app.api.authentication import auth
from app.models.user import User

logger = logging.getLogger(__name__)


class UserApiV1(Resource):

    @auth.login_required
    def get(self):
        print("CURRENT", auth.current_user())
        # user = User.load_user()
        # print(user)
        # user = session["username"
        logger.info("Hello")

        return "Hello"

    @auth.login_required
    def put(self):
        pass

    @auth.login_required
    def delete(self):
        pass
