"""
Author:     David Walshe
Date:       10 May 2021
"""

import logging

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api

from configurations.env_setup import get_config

logger = logging.getLogger(__name__)

# Construct Flask extensions, initialise in factory function.
db = SQLAlchemy()
login_manager = LoginManager()
api_blueprint = Blueprint("api", __name__)
rest_api = Api(api_blueprint)


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

    # Initialise and route Flask-RESTful API for User.
    from .api import UserAPI, UsersAPI, LoginAPI, RegisterAPI
    # rest_api.add_resource(UserAPI, "/api/v1/user", endpoint="user")
    rest_api.add_resource(UsersAPI, "/api/v1/users", endpoint="users")
    rest_api.add_resource(RegisterAPI, "/api/v1/user/register", endpoint="register")

    app.register_blueprint(api_blueprint)

    return app
