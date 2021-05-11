"""
Author:     David Walshe
Date:       10 May 2021
"""

import os

# Path to project root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Parent configuration, common for all configuration setups.
    """
    pass


class DevelopmentConfig(Config):
    """Development Environment"""
    pass


class TestConfig(Config):
    """Test Environment"""
    pass


class ProductionConfig(Config):
    """Production Environment"""
    pass


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
