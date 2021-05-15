"""
Author:     David Walshe
Date:       10 May 2021
"""

import os
import logging

logger = logging.getLogger(__name__)

# Path to project root directory
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """
    Parent configuration, common for all configuration setups.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGER_CONFIG = os.path.join(BASE_DIR, "configurations", "logger", "prod_logger.yml")
    # Set secret key for flask-login sessions
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ADMIN_PASSWORD = os.environ.get("ADMIN_SECRET_KEY")
    TOKEN_EXPIRY = 3600  # 1 Hour

    @classmethod
    def init_app(cls, app):
        logger.debug(f"TOKEN_EXPIRY set to {cls.TOKEN_EXPIRY}")
        os.environ["TOKEN_EXPIRY"] = str(cls.TOKEN_EXPIRY)


class DevelopmentConfig(Config):
    """Development Environment"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or f"sqlite:///{os.path.join(BASE_DIR, 'data-dev.sqlite')}"
    LOGGER_CONFIG = os.path.join(BASE_DIR, "configurations", "logger", "dev_logger.yml")
    TOKEN_EXPIRY = 60


class TestConfig(Config):
    """Test Environment"""
    # Disables error catching during request handling, improves error report output.
    TESTING = True
    # Disables authentication checks for testing, if required.
    LOGIN_DISABLED = False
    # Use a in-memory database for testing.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or "sqlite://"
    TOKEN_EXPIRY = 5


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
