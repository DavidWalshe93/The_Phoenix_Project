# The_Phoenix_Project

> A stepping stone codebase to  working on "Project Unicorn".

[![Build Status](https://travis-ci.com/DavidWalshe93/The_Phoenix_Project.svg?branch=main)](https://travis-ci.com/DavidWalshe93/The_Phoenix_Project)
[![Coverage Status](https://coveralls.io/repos/github/DavidWalshe93/The_Phoenix_Project/badge.svg?branch=main)](https://coveralls.io/github/DavidWalshe93/The_Phoenix_Project?branch=main)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/797fb534d7384d7eb18be57d82416a6d)](https://www.codacy.com/gh/DavidWalshe93/The_Phoenix_Project/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DavidWalshe93/The_Phoenix_Project&amp;utm_campaign=Badge_Grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## TOC

-  [Quickstart Guide](#quickstart-guide)
-  [Requirements](#requirements)
-  [Architecture](#architecture)
-  [Testing](#testing)
-  [CICD Pipeline](#cicd-pipeline)
-  [References](#references)

## Quickstart Guide

## Requirements

-  Create, Update, Delete and List web service endpoints for a User object.
-  User object should contain a name, email address, password and the date of theirlast login.
-  Provide a login endpoint that validates the email address and password provided by the user matches the one stored in
   the database

## Architecture

### Endpoints

| Endpoint            | Method | Auth | Action                                                 |
|---------------------|--------|:----:|--------------------------------------------------------|
| /api/v1/register    | POST   |   🔴  | Registers a new user with the system.                  |
| /api/v1/login       | POST   |   🔴  | Login an existing user.                                |
| /api/v1/users       | GET    |   🔵  | List all user's usernames and last login.              |
| /api/v1/users/me    | GET    |   🔵  | Get a user's own information.                          |
| /api/v1/users/me    | PUT    |   🔵  | Update a user's name or password.                      |
| /api/v1/users/me    | DELETE |   🔵  | Delete a user's account.                               |
| /api/v1/users/<:id> | GET    |   🟢  | Get a single user's username, email and last login.    |
| /api/v1/users/<:id> | PUT    |   🟢  | Update a single user's username, email and last login. |
| /api/v1/users/<:id> | DELETE |   🟢  | Delete a single user.                                  |
| /api/v1/users       | GET    |   🟢  | Get all user's usernames, emails and last logins.      |
| /api/v1/users       | DELETE |   🟢  | Delete a group of users.                               |
| /api/v1/users       | POST   |   🟢  | Create a group of users.                               |

#### Access Rights

| Role       | Access Level |
|------------|:--------------:|
| Anonyomous |       🔴      |
| User       |       🔵      |
| Admin      |       🟢      |

## Testing

## CICD Pipeline

A simple CI/CD flow is created to showcase understanding of core DevOps fundamentals and to keep code honest outside the
original development environment.

### Components

| Component             |  Service  | Links                                                                                                                                                                                                                                                                                                |
|-----------------------|:---------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SCM                   |   GitHub  |                                                                                                                                                                                                                                                                                                      |
| Build Agent           | Travis CI | [![Build Status](https://travis-ci.com/DavidWalshe93/The_Phoenix_Project.svg?branch=main)]( https://travis-ci.com/DavidWalshe93/The_Phoenix_Project )                                                                                                                                                |
| Coverage Analysis     | Coveralls | [![Coverage Status](https://coveralls.io/repos/github/DavidWalshe93/The_Phoenix_Project/badge.svg?branch=main)]( https://coveralls.io/github/DavidWalshe93/The_Phoenix_Project?branch=main )                                                                                                         |
| Code Quality Analysis |   Codacy  | [![Codacy Badge](https://app.codacy.com/project/badge/Grade/797fb534d7384d7eb18be57d82416a6d)]( https://www.codacy.com/gh/DavidWalshe93/The_Phoenix_Project/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DavidWalshe93/The_Phoenix_Project&amp;utm_campaign=Badge_Grade ) |

### Pipeline Architecture

![CICD Architecture](./docs/img/cicd_arch.png)

## Technical References

-  [Flask Web Development, 2nd Edition by Miguel Grinberg](https://learning.oreilly.com/library/view/flask-web-development/9781491991725/)
-  https://blog.miguelgrinberg.com/
-  Stack Overflow

