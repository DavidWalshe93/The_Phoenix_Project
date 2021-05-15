"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask import g
from flask_login import login_required
from flask_restful import Resource

logger = logging.getLogger(__name__)


class UserApiV1(Resource):

    @login_required
    def get(self):
        user = g.current_user
        logger.info("Hello")

        return "Hello"

    @login_required
    def put(self):
        pass

    @login_required
    def delete(self):
        pass
