"""
Author:     David Walshe
Date:       16 May 2021
"""

import logging
from typing import Union, List, Dict, Any

from flask import make_response, request

from app import db
from app.models.user import User
from app.api.authentication import auth, Access
from app.api.errors import bad_request
from app.api.v1.schema import UserSchema, ValidationError

logger = logging.getLogger(__name__)


class DeleteHandler(Handler):

    def __init__(self, id: int):
        """
        Delete endpoint handler.

        :param id: The user id to delete.
        """
        super().__init__(id)

    def handle_user(self):
        """
        As a User, delete your own account.
        """
        logger.debug(f"User closed their account.")
        user: User = auth.current_user()

        user = self.delete(user.id)

        return make_response(user, 204)

    @auth.login_required(role=Access.ADMIN_ONLY())
    def handle_admin(self):
        """
        As an Admin, delete a single account or delete a number of accounts.

        :return: The account ids and usernames that where deleted.
        """
        # Single user deletion
        if self.id:
            user = User.query.filter_by(id=self.id).first()
            ids = user.id
            logger.debug("Admin deleted a single user.")

        # Multi user deletion
        else:
            try:
                # Get user(s) ids to delete.
                users = UserSchema.parse_request(index="users", many=True, only=("id",), as_ns=True)
                ids = [user.id for user in users]
                logger.debug("Admin deleted multiple users.")
            except ValidationError as err:
                msg = UserSchema.parse_validation_error(err)
                return bad_request(msg)

        users = self.delete(ids)

        return make_response(users, 200)

    @staticmethod
    def delete(ids: Union[int, List[int]]) -> Dict[str, Any]:
        """
        Helper method to delete users from the database and return there usernames and ids.

        :param ids: The ids of the users to remove from the database.
        :return: The ids and usernames of the accounts that were deleted.
        """
        # Convert data into common format - List
        if isinstance(ids, int):
            ids = [ids]

        # Get all users for deletion that are currently in DB.
        users = db.session.query(User).where(User.id.in_(ids)).all()

        # DeleteHandler all users passed.
        db.session.query(User).where(User.id.in_(ids)).delete()
        db.session.commit()

        # Return the id, usernames for the deleted users.
        users = UserSchema(many=True, only=("id", "username")).dumps(users)

        return users
