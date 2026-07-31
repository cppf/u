"""Loads the settings needed to start the bot from environment variables."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Holds the settings needed to start the bot."""

    token: str
    port: int
    domain: str


# Placeholder values from deploy_config.py — recognized here so a config
# error message can tell the person exactly what to edit.
_PLACEHOLDER_TOKEN = "REPLACE_WITH_YOUR_BOT_TOKEN_FROM_BOTFATHER"
_PLACEHOLDER_DOMAIN = "REPLACE_IF_NOT_USING_RAILWAY"


def load_config() -> Config:
    """Reads configuration from environment variables only.

    BOT_TOKEN is required; PORT defaults to 8080 if unset.
    """
    return load_config_with_fallback(None, None, None)


def load_config_with_fallback(
    fallback_token: str | None,
    fallback_port: int | None,
    fallback_domain: str | None,
) -> Config:
    """Reads configuration from environment variables, falling back to
    the given values for any variable that is unset or empty in the
    environment. Used by main.py together with deploy_config.py so the
    repository can be deployed with nothing to configure beyond editing
    that one file — environment variables, where present, always take
    priority over the fallback values.
    """
    token = os.environ.get("BOT_TOKEN", "") or (fallback_token or "")
    if not token or token == _PLACEHOLDER_TOKEN:
        raise RuntimeError(
            "No BOT_TOKEN found. Set the BOT_TOKEN environment variable, or edit "
            "deploy_config.py and replace the placeholder token with a real one "
            "from @BotFather."
        )

    port_str = os.environ.get("PORT", "")
    if port_str:
        port = int(port_str)
    else:
        port = fallback_port if fallback_port is not None else 8080

    domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "") or (fallback_domain or "")
    if domain == _PLACEHOLDER_DOMAIN:
        domain = ""

    return Config(token=token, port=port, domain=domain)
