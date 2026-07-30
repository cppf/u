"""Unit tests for the core package: Mode round-tripping and the
deploy_config.py fallback logic in core.config.
"""

import os

from core.mode import Mode
from core.mode_label import mode_label
from core.mode_parse import parse_mode
from core.config import load_config_with_fallback


def test_mode_label_and_parse_mode_round_trip():
    for mode in (Mode.WORD, Mode.SENTENCE, Mode.PARAGRAPH, Mode.FULL):
        label = mode_label(mode)
        assert parse_mode(label) == mode


def test_parse_mode_rejects_unknown_label():
    assert parse_mode("Not a real mode") is None


def test_load_config_rejects_placeholder_token():
    raised = False
    try:
        load_config_with_fallback(
            "REPLACE_WITH_YOUR_BOT_TOKEN_FROM_BOTFATHER", 8080, "example.com"
        )
    except RuntimeError:
        raised = True
    assert raised, "expected RuntimeError for placeholder token"


def test_load_config_uses_fallback_values():
    cfg = load_config_with_fallback("real-token", 9090, "example.com")
    assert cfg.token == "real-token"
    assert cfg.port == 9090
    assert cfg.domain == "example.com"


def test_load_config_env_takes_priority_over_fallback():
    os.environ["BOT_TOKEN"] = "env-token"
    os.environ["PORT"] = "7000"
    try:
        cfg = load_config_with_fallback("fallback-token", 9090, "example.com")
        assert cfg.token == "env-token"
        assert cfg.port == 7000
    finally:
        del os.environ["BOT_TOKEN"]
        del os.environ["PORT"]
