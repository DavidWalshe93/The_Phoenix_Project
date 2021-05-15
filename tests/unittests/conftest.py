"""
Author:     David Walshe
Date:       14 May 2021
"""

from types import ModuleType
from typing import Union

import pytest

from app import create_app
from app.models import User


@pytest.fixture
def app_context():
    """

    Returns a application Creates a Flask application context using a context manager
    for testing Flask dependent functions.

    :return: The Flask application context
    """
    app = create_app("test")

    return app.app_context()


@pytest.fixture
def mock_user_class_for(mocker):
    """
    Pytest fixture for generating Mocked instances of the User Model.

    :return: A mocked User Model.
    """

    class MockedUserMeta(type):
        """
        Meta Class to mock out the static properties of an SQLAlchemy Model.

        Example:
            User.query.filter_by(X).all()  <- All static methods needing mocking.
        """
        staic_instance = mocker.MagicMock(spec=User)

        def __getattr__(self, key):
            return MockedUserMeta.staic_instance.__getattr__(key)

    class MockedUser(metaclass=MockedUserMeta):
        """
        Mocks out an instance of the User model for testing.
        """
        original_cls = User
        instances = []

        def __new__(cls, *args, **kwargs):
            # Adds a new instance of a MockedUser to the instance list.
            MockedUser.instances.append(mocker.MagicMock(spec=MockedUser.original_cls))
            # Return the latest Mocked user.
            MockedUser.instances[-1].__class__ = MockedUser

            # Return the lastest instance.
            return MockedUser.instances[-1]

    def mock(target: Union[str, ModuleType]):
        """
        Mocks a User object for the given target module or module path.

        NOTE: Target should reference the SUT module not the root module.
              i.e.
                Correct: app.api.authentication.User
                Wrong:   app.models.user.User


        :param target: Can be a module reference or a dot notation string to the reference.
        :return: The mocked instance.
        """
        if isinstance(target, ModuleType):
            # Mocks based on a based SUT module.
            return mocker.patch(f"{target.__name__}.User", new=MockedUser)
        else:
            # Mocks based on a target module path.
            return mocker.patch(target, new=MockedUser)

    return mock
