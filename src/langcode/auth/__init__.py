"""Authentication credential storage."""

from langcode.auth.auth import (
    OAUTH_DUMMY_KEY,
    ApiAuth,
    Auth,
    AuthInfo,
    OAuth,
    WellKnownAuth,
    all_credentials,
    get_credential,
    remove_credential,
    set_credential,
)

__all__ = [
    "OAUTH_DUMMY_KEY",
    "ApiAuth",
    "Auth",
    "AuthInfo",
    "OAuth",
    "WellKnownAuth",
    "all_credentials",
    "get_credential",
    "remove_credential",
    "set_credential",
]
