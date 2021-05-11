"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging

from . import user
from .. import db

logger = logging.getLogger(__name__)


@user.route("/user", methods=["GET"])
def get_user():
    return "John Smith"

