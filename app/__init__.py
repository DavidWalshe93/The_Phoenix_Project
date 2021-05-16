"""
Author:     David Walshe
Date:       10 May 2021
"""

import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api

from configurations.env_setup import get_config
from app.common.logger import init_logger

init_logger(get_config("dev").LOGGER_CONFIG)

logger = logging.getLogger(__name__)

# Construct Flask extensions, initialise in factory function.
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name: str = "dev") -> Flask:
    """
    Application factory function to create a Flask application instance.

    Allows various configurations to be injected to easily enable dev/test/prod instance creation.

    :param config_name: The username of the configuration to use. Default: "dev".
    :return: An application instance with the desired environment configuration settings.
    """
    app = Flask(__name__)

    app = setup_env(app, config_name)

    app = init_plugins(app)

    app = setup_api(app)

    return app


def setup_env(app: Flask, config_name: str) -> Flask:
    """
    Sets the application environment for the Flask object.
    :param app: The Flask object.
    :param config_name: The configuration environment to use.
    :return: The Flask object.
    """
    # Get environment configuration.
    config = get_config(config_name)
    # Inject configuration into application instance.
    app.config.from_object(config)
    # Initialise application configuration settings if required.
    config.init_app(app)

    return app


def init_plugins(app: Flask) -> Flask:
    """
    Initialises Flask plugins.

    :param app: The Flask object.
    :return: The Flask object.
    """
    # Initialise Database.
    db.init_app(app)
    db.create_all(app=app)

    try:
        with app.app_context():
            # Add roles to database
            from app.models import Role
            _ = [db.session.add(Role(name=role)) for role in ["user", "admin"]]

            db.session.commit()
    except Exception:
        logger.debug(f"Role table already setup.")

    # Initialise Marshmallow
    ma.init_app(app)

    return app


def setup_api(app: Flask) -> Flask:
    """
    Sets up the API Blueprint, Flask-RESTful API and Routing.

    :param app: The Flask object.
    :return: The
    """
    # Initialise and route Flask-RESTful API for User.
    from .api import get_blueprint, UserApiV1, UsersApiV1, LoginApiV1, RegisterApiV1
    api_bp = get_blueprint()
    api = Api(api_bp)

    # Setup API Routes/Endpoints.
    # api.add_resource(UsersApiV1, "/api/v1/users/me", endpoint="user")
    api.add_resource(UsersApiV1, "/api/v1/users/<string:id>", endpoint="user")
    api.add_resource(UsersApiV1, "/api/v1/users", endpoint="users")
    api.add_resource(UsersApiV1, "/api/v1/users/<int:id>", endpoint="users_id")
    api.add_resource(RegisterApiV1, "/api/v1/register", endpoint="register")
    api.add_resource(LoginApiV1, "/api/v1/login", endpoint="login")

    app.register_blueprint(api_bp)

    return app
