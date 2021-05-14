"""
Author:     David Walshe
Date:       14 May 2021
"""

import pytest
from contextlib import contextmanager

from app import create_app


@pytest.fixture
def app_context():
    """

    Returns a application Creates a Flask application context using a context manager
    for testing Flask dependent functions.

    :return: The Flask application context
    """
    app = create_app("test")

    return app.app_context()
