"""Authentication credential storage and management."""

import json
import logging
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from langcode.config.globals import Global
from langcode.util.filesystem import Filesystem

OAUTH_DUMMY_KEY = "langcode-oauth-dummy-key"


class OAuth(BaseModel):
    """OAuth authentication credentials."""

    type: Literal["oauth"] = "oauth"
    refresh: str
    access: str
    expires: int
    account_id: str | None = Field(None, alias="accountId")
    enterprise_url: str | None = Field(None, alias="enterpriseUrl")

    class Config:
        populate_by_name = True


class ApiAuth(BaseModel):
    """API key authentication."""

    type: Literal["api"] = "api"
    key: str


class WellKnownAuth(BaseModel):
    """Well-known authentication with key and token."""

    type: Literal["wellknown"] = "wellknown"
    key: str
    token: str


AuthInfo = Annotated[OAuth | ApiAuth | WellKnownAuth, Field(discriminator="type")]


class Auth:
    """Authentication credential storage."""

    _filepath = Path(Global.Path.data) / "auth.json"

    @classmethod
    async def get(cls, provider_id: str) -> AuthInfo | None:
        """Get authentication credentials for a provider.

        Args:
            provider_id: Provider identifier

        Returns:
            Authentication info if found, None otherwise
        """
        auth = await cls.all()
        return auth.get(provider_id)

    @classmethod
    async def all(cls) -> dict[str, AuthInfo]:
        """Get all authentication credentials.

        Returns:
            Dictionary mapping provider IDs to authentication info
        """
        try:
            content = await Filesystem.read(str(cls._filepath))
            data = json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

        result: dict[str, AuthInfo] = {}
        for key, value in data.items():
            try:
                # Try each type in order
                if isinstance(value, dict):
                    auth_type = value.get("type")
                    if auth_type == "oauth":
                        result[key] = OAuth(**value)
                    elif auth_type == "api":
                        result[key] = ApiAuth(**value)
                    elif auth_type == "wellknown":
                        result[key] = WellKnownAuth(**value)
            except Exception as e:
                logging.debug("Skip invalid auth entry %s: %s", key, e)
                continue

        return result

    @classmethod
    async def set(cls, key: str, info: AuthInfo) -> None:
        """Set authentication credentials for a provider.

        Args:
            key: Provider identifier
            info: Authentication information
        """
        normalized = key.rstrip("/")
        data = await cls.all()

        # Remove both original and normalized keys with trailing slash
        if normalized != key:
            data.pop(key, None)
        data.pop(normalized + "/", None)

        # Set normalized key - convert Pydantic model to dict
        data[normalized] = info

        # Convert all Pydantic models to dicts for JSON serialization
        json_data = {k: v.model_dump(by_alias=True) for k, v in data.items()}

        # Write to file with restricted permissions
        await Filesystem.write_json(str(cls._filepath), json_data, mode=0o600)

    @classmethod
    async def remove(cls, key: str) -> None:
        """Remove authentication credentials for a provider.

        Args:
            key: Provider identifier
        """
        normalized = key.rstrip("/")
        data = await cls.all()

        # Remove both original and normalized keys
        data.pop(key, None)
        data.pop(normalized, None)

        # Convert all Pydantic models to dicts for JSON serialization
        json_data = {k: v.model_dump(by_alias=True) for k, v in data.items()}

        await Filesystem.write_json(str(cls._filepath), json_data, mode=0o600)


# Convenience functions
async def get_credential(provider_id: str) -> AuthInfo | None:
    """Get authentication credentials for a provider."""
    return await Auth.get(provider_id)


async def all_credentials() -> dict[str, AuthInfo]:
    """Get all authentication credentials."""
    return await Auth.all()


async def set_credential(key: str, info: AuthInfo) -> None:
    """Set authentication credentials for a provider."""
    await Auth.set(key, info)


async def remove_credential(key: str) -> None:
    """Remove authentication credentials for a provider."""
    await Auth.remove(key)
