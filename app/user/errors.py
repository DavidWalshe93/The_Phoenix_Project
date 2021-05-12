"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging

from . import user

logger = logging.getLogger(__name__)


@user.app_errorhandler(404)
def resource_not_found(e):
    return "Resource not found", 404
