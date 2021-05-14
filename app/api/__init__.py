"""
Author:     David Walshe
Date:       13 May 2021
"""

from .endpoints import get_blueprint
from .v1.ep.login import LoginAPI
from .v1.ep.register import RegisterAPI
from .v1.ep.user import UserAPI
