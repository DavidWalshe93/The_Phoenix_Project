"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

from flask_login import login_required
from flask_restful import Resource

logger = logging.getLogger(__name__)


class UserAPI(Resource):

    def get(self):
        pass

    @login_required
    def put(self):
        pass

    def delete(self):
        pass
