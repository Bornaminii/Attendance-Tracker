"""Settings for the local/CI test suite. Uses SQLite so Postgres is not required."""

from .base import *  # noqa: F403

DEBUG = False
SECRET_KEY = "test-secret-key"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
