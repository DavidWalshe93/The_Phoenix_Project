"""
Author:     David Walshe
Date:       13 May 2021
"""

from typing import Generator
from dataclasses import dataclass
from contextlib import contextmanager

from flask import Flask
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
