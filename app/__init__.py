"""
Author:     David Walshe
Date:       10 May 2021
"""

import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api

from configurations.env_setup import get_config

logger = logging.getLogger(__name__)

# Construct Flask extensions, initialise in factory function.
db = SQLAlchemy()
login_manager = LoginManager()
auth = HTTPBasicAuth()
api = Api()


def create_app(config_name: str = "dev") -> Flask:
    """
    Factory function to create an application instance.

    Allows various configurations to be injected to easily enable dev/test/prod instance creation.

    :param config_name: The name of the configuration to use. Default: "dev".
    :return: An application instance with the desired environment configuration settings.
    """
    app = Flask(__name__)

    # Get environment configuration.
    config = get_config(config_name)

    # Inject configuration into application instance.
    app.config.from_object(config)

    # Initialise application configuration settings if required.
    config.init_app(app)

    # Initialise Database.
    db.init_app(app)
    db.create_all(app=app)

    # Initialise LoginManager
    login_manager.init_app(app=app)

    # Initialise HTTPAuth

    # Initialise and route Flask-RESTful API for User.
    from .user import UserAPI, UsersAPI
    api.add_resource(UserAPI, "/api/v1/user", endpoint="user")
    api.add_resource(UsersAPI, "/api/v1/users", endpoint="users")

    api.init_app(app=app)

    # Add user blueprint to application
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    return app
