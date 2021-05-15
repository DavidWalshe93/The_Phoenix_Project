"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging
from types import ModuleType
from datetime import datetime

import pytest


@pytest.fixture(autouse=True)
def set_log_level(caplog):
    """Set the log level for the test session."""
    caplog.set_level(logging.DEBUG)


@pytest.fixture
def fake_user() -> dict:
    """Returns a fake user dictionary."""
    return {
        "email": "calvin.crawford@example.com",
        "name": "crazywolf900",
        "password": "cricket",
        "last_login": datetime(year=2021, month=5, day=15, hour=10, minute=51, second=20)
    }


@pytest.fixture
def target_factory() -> callable:
    """
    Factory function for creating mock target paths from a given SUT module.

    :return: A callable to create target paths.
    """

    def target(sut: ModuleType, attribute: str) -> str:
        """
        Returns the dotted string notation path meeting the requirements for a
        unittest.mock.patch call.

        :param sut: The module under test.
        :param attribute: The attribute to patch with a MagicMock.
        :return: A dotted notation string to reference the module.attribute to mock.
        """
        return f"{sut.__name__}.{attribute}"

    return target
