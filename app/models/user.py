"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging

from .. import db

logger = logging.getLogger(__name__)


class User(db.Model):
    """Models a User object from a users SQL table."""
    __tablename__ = "users"

    # User columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    last_login = db.Column(db.DateTime)

    def __repr__(self) -> str:
        """Return string representation of User object."""
        return f"<User {self.name} - {self.last_login}>"
