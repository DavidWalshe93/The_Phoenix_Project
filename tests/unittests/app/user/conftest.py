"""
Author:     David Walshe
Date:       12 May 2021
"""

import pytest
from datetime import datetime
from typing import List, Dict, Union

from flask.testing import Client

from app import create_app, db
from app.models import User


@pytest.fixture
def users() -> callable:
    """
    Creates and returns a list of users as dictionaries.

    :return: A callable for creating a list of user objects.
    """

    def factory(size: int = 3, datetime_as_string: bool = False, include_password: bool = False) -> List[Dict[str, Union[str, datetime]]]:
        """
        :param size: The number of User dictionary instances to return.
        :param datetime_as_string: Convert datatime to string representation.
        :param include_password: Include user passwords in returned dictionary objects.
        :return: A list of user dictionaries.
        """
        # Return only the number of instances requested by the user.
        names = [name for idx, name in enumerate(["John Smith", "Mary Murphy", "Mike O'Shea"]) if idx < size]

        # Generate 'last_login" times.
        epoch = 1620766488  # Tue, 11 May 2021 21:54:48 GMT
        times = [datetime.fromtimestamp(epoch + delta) for delta in [0, 60, 120]]

        # Convert time into human readable text if required for comparisons.
        if datetime_as_string:
            date_format = "%a, %d %b %Y %H:%M:%S GMT"  # Tue, 11 May 2021 21:54:48 GMT
            times = [f"{time.strftime(date_format)}" for time in times]

        # Create users
        users = [dict(name=user, email=f"{user}@example.com", last_login=time) for user, time in zip(names, times)]

        # Enrich dictionary with user password information if required.
        if include_password:
            users = [dict(**user, password="".join(reversed(user["name"]))) for user in users]

        return users

    return factory


@pytest.fixture
def setup_db(users) -> callable:
    """
    Sets up the testing database and adds some User instances.

    :param users: A list of user dictionaries.
    :return: A factory function to create a database.
    """

    def _setup_db(size: int = 3):
        """
        Creates and populates a in-memory database for testing.

        :param size: The number of users to add to the database.
        """
        # Creates tables in Database.
        db.create_all()
        # Create a list of User Models.
        user_models = [User(**user) for user in users(size=size, include_password=True)]
        # Add the User Models to the Database
        [db.session.add(user) for user in user_models]
        # Commit the changes.
        db.session.commit()

    return _setup_db


@pytest.fixture
def client_factory(setup_db: callable) -> callable:
    """
    Supplies a flask client object to test the REST endpoints of the application.

    :param setup_db: Function to setup testing database.
    :return: A factory function for creating a Flask Client object.
    """

    def factory(size: int = 3) -> Client:
        """
        Creates and initialises a client object.

        :param size: The number of instance to add to the database for testing.
        :return: A Flask Client object.
        """
        app = create_app("test")

        with app.test_client() as client:
            with app.app_context():
                setup_db(size=size)

            return client

    return factory
