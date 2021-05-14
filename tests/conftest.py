"""
Author:     David Walshe
Date:       14 May 2021
"""

import logging

import pytest


@pytest.fixture(autouse=True)
def set_log_level(caplog):
    """Set the log level for the test session."""
    caplog.set_level(logging.DEBUG)
