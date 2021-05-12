#!/bin/bash

# David Walshe
# 11-May-2021

# Shell script to setup environment variables to run application locally.

# Set Flask application entry point
# ---------------------------------
export FLASK_APP=run.py

# Set Flask Debug mode
# --------------------
export FLASK_DEBUG=1