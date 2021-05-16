"""
Author:     David Walshe
Date:       13 May 2021
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass, field
from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from copy import deepcopy

from requests.auth import _basic_auth_str
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask.testing import Client

from app.models import User


@dataclass
class AttributeFilter:
    keep_password: bool
    keep_role_id: bool
    keep_role_name: bool
    keep_email: bool
    admin_only: bool

    @classmethod
    def make(cls, **kwargs):
        """Factory method for creating and returning a Attribute Filter."""
        return cls(
            keep_password=kwargs.get("keep_password", False),
            keep_role_id=kwargs.get("keep_role_id", False),
            keep_role_name=kwargs.get("keep_role_name", False),
            keep_email=kwargs.get("keep_email", True),
            admin_only=kwargs.get("admin_only", False)
        )


def filter_attributes(func):
    """Filters and removes attributes from User Dictionary objects depending on test requirements."""

    @wraps(func)
    def filter_attributes_wrapper(*args, **kwargs):
        # Get generated users.
        users = func(*args, **kwargs)

        # If only single user (dict), treat as a list for filtering.
        unpack = False
        if not isinstance(users, list):
            users = [users]
            unpack = True

        # Create filter instance.
        filter = AttributeFilter.make(**kwargs)

        # Apply filters
        if not filter.keep_password:
            _ = [user.pop("password") for user in users]

        if filter.admin_only:
            users = [user for user in users if user.get("role_id", 1) == 2]

        if filter.keep_role_name:
            _ = [user.update({"role_name": "admin" if user["role_id"] == 2 else "user"}) for user in users]

        if not filter.keep_role_id:
            _ = [user.pop("role_id") for user in users]

        if not filter.keep_email:
            _ = [user.pop("email") for user in users]

        # If single instance used, unpack it back to a single dict.
        if unpack:
            return users[0]

        return users

    return filter_attributes_wrapper


@dataclass
class FlaskTestRig:
    """
    Flask application testing rig. Uses to encapsulate helpful datapoints required for testing
    under the one namespace.

    :param client: The Flask Client for running requests off endpoints.
    :param app: The Flask Application instance.
    :param db: The SQLAlchemy database instance.
    :param User: The User model reference.
    :param db_entries: A list of dictionaries describing the current state of the database.
    :param make_users: A callable used to create new users during tests if required.
    """
    client: Client
    app: Flask
    db: SQLAlchemy
    User: User
    db_entries: List[Dict[str, Any]] = field(default_factory=[])
    make_users: callable = None

    @classmethod
    def create(cls, client_factory: callable, make_users: callable, n_users: int = 3):
        """
        Factory method to create a FlaskTestRig from a generator.

        :param client_factory: A generator of one item, holding the flask test context.
        :param make_users: Callable to create users with.
        :param n_users: The number of users to create.
        :return: A FlaskTestRig object.
        """
        users = make_users(n_users)

        generator = client_factory(users)

        client, app, db, user = next(generator)

        return cls(
            client=client,
            app=app,
            db=db,
            User=user,
            db_entries=users,
            make_users=make_users
        )

    @contextmanager
    def app_context(self):
        """
        Exposes the app.app_context for flask as a context manager.

        :return: The application context object.
        """
        with self.app.app_context() as ctx:
            yield ctx

    @staticmethod
    def extract_rig_from_kwargs(key_word_args: dict) -> object:
        """
        Extracts the FlaskTestRig object from the kwargs of a test.

        :param key_word_args: The key-word argument dictionary containing the FlaskTestRig object.
        :return: The extracted FlaskTestRig object.
        """
        return key_word_args["rig"]

    @filter_attributes
    def get_current_users(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Returns a list of dictionaries describing all users in the current Database.

        :return: A list of dictionaries describing all users in the current Database.
        """
        users = deepcopy(self.db_entries)

        return users

    def get_first_user(self, **kwargs) -> Dict[str, Any]:
        """
        Returns the first existing user in the db_entries for this Flask application session.

        :return: A dictionary describing a current User.
        """
        return self.get_current_users(**kwargs)[0]

    @filter_attributes
    def create_new_user(self, **kwargs) -> Dict[str, Any]:
        """
        Returns the newly generated user not in the current db of the application.

        :return: A dictionary describing a new User.
        """
        admin_only = kwargs.get("admin_only", False)

        return self.make_users(1, admin_only=admin_only)[0]

    @staticmethod
    def setup_app(n_users: int = 3):
        """
        Sets up a REST API test by creating a FlaskTestRig object and adding users to the test database.

        :param n_users: The number of users to add to the database.
        :return: The
        """

        def _setup_app(func):
            @wraps(func)
            def setup_app_wrapper(*args, **kwargs):
                # Pull setup functions from kwargs
                client_factory = kwargs["client_factory"]
                make_users = kwargs["make_users"]

                rig = FlaskTestRig.create(client_factory=client_factory, make_users=make_users, n_users=n_users)

                return func(rig=rig, **kwargs)

            return setup_app_wrapper

        return _setup_app


def login(client: Client, user: dict, should_fail: bool = False) -> str:
    """
    Logs a user in to test login protected resources.

    :param client: The Flask Client object.
    :param user: A user to login with.
    :param should_fail: Should not be able to login as this user.
    :return: The token to send requests with.
    """
    response: Response = client.post("/api/v1/login",
                                     data=dict(
                                         email=user.get("email"),
                                         password=user.get("password")
                                     ))

    token = json.loads(response.data).get("token")

    if should_fail:
        # Assert token was not acquirable.
        assert response.status_code == 400
        assert token == None
    else:
        # Assert token was acquired before continuing testing.
        assert response.status_code == 200
        assert token != None

    return token


def basic_auth_header_password(email: str, password: str) -> Dict[str, str]:
    """
    Returns the "Authorization" header and token for use in a request.

    :param email: The basic authorization email.
    :param password: The basic authorization password.
    :return: A authorization header dictionary.
    """
    return {"Authorization": _basic_auth_str(email, password)}


def basic_auth_header_token(username: str, password: str) -> Dict[str, str]:
    """
    Basic Authentication.

    Returns the "Authorization" header and username/password for use in a request.

    :param username: The basic authorization username.
    :param password: The basic authorization password.
    :return: A authorization header dictionary.
    """
    return {"Authorization": _basic_auth_str(username, password)}


def token_auth_header_token(token: str) -> Dict[str, str]:
    """
    Bearer Token Authentication.

    Returns the "Authorization" header and token for use in a request.

    :param token: The basic authorization token.
    :return: A authorization header dictionary.
    """
    return {"Authorization": f"Bearer {token}"}


def datetime_as_string(time: datetime) -> str:
    """
    Convert time into human readable text if required for comparisons.

    :param time: The datetime object to convert.
    :return: The datetime objects time as a formatted string.
    """
    date_format = "%a, %d %b %Y %H:%M:%S GMT"  # Tue, 11 May 2021 21:54:48 GMT
    date_format = "%Y-%m-%dT%H:%M:%S"  # 2021-05-11T21:56:48

    return f"{time.strftime(date_format)}"
