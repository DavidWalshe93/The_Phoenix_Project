"""
Author:     David Walshe
Date:       13 May 2021
"""

import json
from typing import Generator, Dict
from dataclasses import dataclass
from contextlib import contextmanager
from datetime import datetime

from requests.auth import _basic_auth_str
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask.testing import Client

from app.models import User


@dataclass
class FlaskTestRig:
    client: Client
    app: Flask
    db: SQLAlchemy
    User: User

    @classmethod
    def create(cls, generator: Generator):
        """
        Factory method to create a FlaskTestRig from a generator.

        :param generator: A generator of one item, holding the flask test context.
        :return: A FlaskTestRig object.
        """
        client, app, db, user = next(generator)

        return cls(
            client=client,
            app=app,
            db=db,
            User=user
        )

    @contextmanager
    def app_context(self):
        """
        Exposes the app.app_context for flask as a context manager.

        :return: The application context object.
        """
        with self.app.app_context() as ctx:
            yield ctx


def login(client: Client, user: dict) -> str:
    """
    Logs a user in to test login protected resources.

    :param client: The Flask Client object.
    :param user: A user to login with.
    :return: The token to send requests with.
    """
    response: Response = client.post("/api/v1/user/login",
                                     data=dict(
                                         email=user.get("email"),
                                         password=user.get("password")
                                     ))

    token = json.loads(response.data).get("token")
    print(token)
    assert response.status_code == 200
    assert token != None

    print(token)

    return token


def basic_auth_header_password(email: str, password: str) -> Dict[str, str]:
    """
    Returns the "Authorization" header and token for use in a request.

    :param email: The basic authorization email.
    :param password: The basic authorization password.
    :return: A authorization header dictionary.
    """
    return {"Authorization": _basic_auth_str(email, password)}


def basic_auth_header_token(token: str) -> Dict[str, str]:
    """
    Returns the "Authorization" header and token for use in a request.

    :param token: The basic authorization token.
    :return: A authorization header dictionary.
    """
    return {"Authorization": _basic_auth_str(token, "")}


def datetime_as_string(time: datetime) -> str:
    """
    Convert time into human readable text if required for comparisons.

    :param time: The datetime object to convert.
    :return: The datetime objects time as a formatted string.
    """
    date_format = "%a, %d %b %Y %H:%M:%S GMT"  # Tue, 11 May 2021 21:54:48 GMT

    return f"{time.strftime(date_format)}"
