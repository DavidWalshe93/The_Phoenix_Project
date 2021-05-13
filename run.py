"""
Author:     David Walshe
Date:       11 May 2021
"""

import logging
import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import User

logger = logging.getLogger(__name__)

# Create application instance using application factory.
app = create_app(os.getenv("FLASK_CONFIG") or "default")

# Create database migration.
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
