"""
Author:     David Walshe
Date:       13 May 2021
"""

import requests
import yaml
from dataclasses import dataclass, asdict


@dataclass
class User:
    username: str
    email: str
    password: str
    role_id: int


# API PARAMS
NUM_USERS = 50
FORMAT = "pretty"
NATIONALITY = "us,ie,gb"
INCLUDE = "username,email,login"


def generate_users():
    """
    Downloads NUM_USERS from the randomuser API and saves them to disk to use in testing.
    """
    url = f"https://randomuser.me/api/?results={NUM_USERS}&format={FORMAT}&nat={NATIONALITY}&inc={INCLUDE}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()

    # Save only required information.
    users = []
    for user in data["results"]:
        username = user["login"]["username"]
        email = user["email"]
        password = user["login"]["password"]
        role_id = 1  # All user roles

        users.append(asdict(User(username, email, password, role_id)))

    with open("users.yml", "w") as fh:
        yaml.safe_dump(users, fh)


if __name__ == '__main__':
    generate_users()
