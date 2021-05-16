"""
Author:     David Walshe
Date:       12 May 2021
"""

import pytest
from datetime import datetime
from typing import List, Dict, Union, Any

import yaml
from flask.testing import Client

from app import create_app, db
from app.models import User, Role


@pytest.fixture(scope="session")
def load_users():
    with open("./tests/data/users.yml") as fh:
        return yaml.safe_load(fh)


@pytest.fixture
def make_users(load_users) -> callable:
    """
    Creates and returns a list of users as dictionaries.

    :return: A callable for creating a list of user objects.
    """
    users = load_users

    # Create a generator of users.
    _users = (user for user in users)

    def factory(size: int = 3, admin_only: bool = False) -> List[Dict[str, Union[str, datetime]]]:
        """
        :param size: The number of User dictionary instances to return.
        :param admin_only: Make all generated user's have the admin role.
        :return: A list of user dictionaries.
        """
        # Return only the number of instances requested by the user.
        try:
            user_batch = [next(_users) for _ in range(size)]
        except StopIteration:
            raise StopIteration("No more names to yield in names generator. (Max==50)")

        # Generate 'last_login" times for each user.
        epoch = 1620766488  # Tue, 11 May 2021 21:54:48 GMT
        deltas = [t * 60 for t in range(0, len(user_batch))]
        times = [datetime.fromtimestamp(epoch + delta) for delta in deltas]

        # Append last_login time to users.
        user_batch = [{**user, "last_login": time} for user, time in zip(user_batch, times)]

        if admin_only:
            user_batch = [{**user, "role_id": 2} for user in user_batch]

        return user_batch

    return factory


@pytest.fixture
def init_db() -> callable:
    """
    Sets up the testing database and adds some User instances.

    :return: A factory function to create a database.
    """

    def _setup_db(users: List[Dict[str, Any]]):
        """
        Creates and populates an in-memory database for testing.

        :param size: The number of users to add to the database.
        """
        # Creates tables in Database.
        db.drop_all()
        db.create_all()
        if users is not None:
            # Create a list of User Models.
            user_models = [User(**user) for user in users]
            # Add the User Models to the Database
            _ = [db.session.add(user) for user in user_models]

        # Add roles to database
        _ = [db.session.add(Role(name=role)) for role in ["user", "admin"]]

        # Commit the changes.
        db.session.commit()

        return db

    return _setup_db


@pytest.fixture
def client_factory(init_db) -> callable:
    """
    Supplies a flask client object to test the REST endpoints of the application.

    :param init_db: Function to setup testing database.
    :return: A factory function for creating a Flask Client object.
    """

    def factory(users: List[Dict[str, Any]] = None) -> Client:
        """
        Creates and initialises a client object.

        :param users: The users to add to the test database.
        :return: A Flask Client object.
        """
        app = create_app("test")

        with app.test_client() as client:
            with app.app_context():
                init_db(users=users)

                # Return context objects.
                yield client, app, db, User

                # Clean up database
                db.session.remove()
                db.drop_all()

    return factory


@pytest.fixture
def database():
    """Returns the database object as a test fixture."""
    return db


@pytest.fixture
def user_model():
    """Returns the User model object as a test fixture."""
    return User
