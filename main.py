"""Entry point — wires everything together."""

import logging

import deploy_config

from core.config import load_config_with_fallback
from stats.db import init_db
from stats.register_stats_handlers import register_stats_handlers
from stats.track_middleware import register_track_middleware

from telegram_ui.main_menu import new_main_menu
from telegram_ui.new_bot import new_bot
from telegram_ui.register_content_handlers import register_content_handlers
from telegram_ui.register_main_menu_handlers import register_main_menu_handlers
from telegram_ui.register_settings_handlers import register_settings_handlers
from telegram_ui.settings_menu import new_settings_menu
from telegram_ui.store import new_store
from telegram_ui.webhook_url import webhook_url


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    cfg = load_config_with_fallback(
        deploy_config.BOT_TOKEN,
        deploy_config.PORT,
        deploy_config.RAILWAY_PUBLIC_DOMAIN,
    )

    init_db()

    app = new_bot(cfg.token)

    # Registered in its own earlier handler group so every update is
    # counted no matter which other handler also processes it — see
    # track_middleware.py for why this differs from a single bot.Use(...)
    # call in the Go version.
    register_track_middleware(app)

    st = new_store()

    main_menu, main_btns = new_main_menu()
    settings_menu, settings_btns = new_settings_menu()

    register_main_menu_handlers(app, st, main_btns, main_menu, settings_btns, settings_menu)
    register_settings_handlers(app, st, settings_btns, main_menu)
    register_content_handlers(app, st, main_menu)
    register_stats_handlers(app, settings_btns)

    logger.info("bot started")

    # PTB's run_webhook starts its own HTTP server (no separate Flask/
    # FastAPI app needed) and registers the webhook URL with Telegram,
    # mirroring telebot.v3's built-in Webhook poller.
    app.run_webhook(
        listen="0.0.0.0",
        port=cfg.port,
        url_path=cfg.token,
        webhook_url=webhook_url(cfg.domain, cfg.token),
    )


if __name__ == "__main__":
    main()
