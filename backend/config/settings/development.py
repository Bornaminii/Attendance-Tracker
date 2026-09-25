"""Local and Docker development settings."""

from .base import *  # noqa: F403

DEBUG = env.bool("DEBUG", default=True)  # noqa: F405
