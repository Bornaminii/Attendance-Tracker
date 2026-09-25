"""Production settings. Secrets and hosts must come from the environment."""

from .base import *  # noqa: F403

DEBUG = False

if SECRET_KEY == "dev-only-change-me":  # noqa: F405
    raise ValueError("SECRET_KEY must be set in production.")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
