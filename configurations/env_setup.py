"""
Author:     David Walshe
Date:       10 May 2021
"""

import os

# Path to project root directory
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """
    Parent configuration, common for all configuration setups.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Development Environment"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or f"sqlite:///{os.path.join(BASE_DIR, 'data-dev.sqlite')}"


class TestConfig(Config):
    """Test Environment"""
    # Disables error catching during request handling, improves error report output.
    TESTING = True
    # Use a in-memory database for testing.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or f"sqlite://"


class ProductionConfig(Config):
    """Production Environment"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'data.sqlite')}"


def get_config(env: str = None) -> Config:
    """
    Retrieves the requested environment object ([dev]/test/prod).

    If no environment string is specified, falls back to DevelopmentConfig

    :param env: A string denoting the environment to be returned.
    :return: An environment object, matching the user's specification,
             if not specified or does not match, returns the dev environment by default.
    """
    return {
        "dev": DevelopmentConfig,
        "test": TestConfig,
        "prod": ProductionConfig
    }.get(env, DevelopmentConfig)
