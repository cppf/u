"""Builds the public webhook URL Telegram uses to deliver updates."""


def webhook_url(domain: str, token: str) -> str:
    """Builds the public URL Telegram will use to deliver updates.

    Combines Railway's public domain with the bot token as the path secret.
    """
    return f"https://{domain}/{token}"
