import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Global SQLAlchemy instance that can be imported by the rest of the project
# Scripts such as ``init_db.py`` and ``fix_material_table.py`` rely on this
# object being available at ``app.db``.
db = SQLAlchemy()


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory for the Approver web application.

    The function configures a Flask application instance, initialises the
    database layer and ensures that the ORM models are imported so that SQLAlchemy
    is aware of them before ``create_all`` is executed by the maintenance
    scripts.
    """

    app = Flask(__name__)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///approver.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    # Import models so they are registered with SQLAlchemy. Importing inside the
    # factory avoids circular import issues while keeping the module level
    # ``db`` instance accessible to callers importing ``app``.
    from . import models  # noqa: F401  # pylint: disable=unused-import

    return app
