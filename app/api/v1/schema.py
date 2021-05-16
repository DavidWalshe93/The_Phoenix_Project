"""
Author:     David Walshe
Date:       16 May 2021
"""

import logging
import json
from json.decoder import JSONDecodeError
import re
from typing import List, Dict, Union
from types import SimpleNamespace
from datetime import datetime
from dataclasses import dataclass

from flask import Request, jsonify, request
from marshmallow import fields, validates, validate, ValidationError, Schema, INCLUDE

from werkzeug.security import generate_password_hash

from app import ma
from app.models import User

logger = logging.getLogger(__name__)


@dataclass
class UserDescriptor:
    """Used to add code completion to SimpleNamespace."""
    id: int
    username: str
    email: str
    password: str
    password_hash: str
    last_login: datetime
    role: int
    role_name: str


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        # Allow auto-field mapping to SQL Alchemy Model.
        model = User
        unknown = INCLUDE
        include_fk = True

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field(validate=validate.Email())
    password = fields.String()
    password_hash = ma.auto_field()
    last_login = ma.auto_field()
    role = ma.auto_field()
    role_id = fields.Method("init_role_id")
    role_name = fields.Method("init_role_name")

    def init_role_id(self, obj):
        """Initialisation method to set the role id from a User object."""
        if isinstance(obj, dict):
            return obj["role_id"]
        else:
            return obj.role.id

    def init_role_name(self, obj):
        """Initialisation method to set the role name from a User object."""
        if isinstance(obj, dict):
            return obj["role_name"]
        else:
            return obj.role.name

    def jsonify(self, data) -> str:
        """
        Return the dumped object(s) as a json string.

        :return: User object(s) as a JSON string.
        """
        return jsonify(self.dump(data))

    @classmethod
    def parse_request(cls, *, index: str = None, many: bool = False, only: tuple = None, as_ns=False) -> Union[dict, UserDescriptor, List[UserDescriptor]]:
        """
        Parses the data from a client request and generates a UserSchema object.

        :param index: Index path to User object data.
        :param many: Flag to denote more than one User to parse.
        :param only: Whitelist of attributes to return.
        :param as_ns: Return as a SimpleNamespace object instead of a dictionary.
        :return: A UserSchema object with the request data set internally.
        """

        def indexer(d: dict, keys: list):
            """
            Recursive dictionary traverser for given key set.

            :param d: The current data dictionary.
            :param keys: The keys to traverse.
            :return: The leaf node of the dictionary accessed by the keys.
            """
            try:
                key = keys.pop()
                return indexer(d[key], keys)
            except IndexError:
                return d

        # Read data from values.
        data = request.values

        if not data:
            try:
                # Get the request data as a dictionary.
                data = json.loads(request.data)
            except JSONDecodeError:
                return None

        # If traversal is required to internal keys.
        if index is not None:
            keys = list(reversed(index.split(".")))
            data = indexer(data, keys)

        data = cls(only=only).load(data, many=many)

        # Map data to User Schema.
        if as_ns:
            # Create a list of SimpleNamespaces if data is a list.
            if isinstance(data, list):
                return [SimpleNamespace(**item) for item in data]

            # Return SimpleNamespace
            return SimpleNamespace(**data)

        # Return Dictionary.
        return data

    @staticmethod
    def parse_validation_error(err: ValidationError) -> Dict[str, List[str]]:
        """
        Parses the contents of a Validation error and returns it in
        a format suitable for a Bad Request response to the client.

        :param err: The Validation error to parse.
        :return: A response ready error format.
        """
        errors = list(err.messages.values())
        errors = {list(item.keys())[0]: list(item.values())[0] for item in errors}

        return errors
