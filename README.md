# Monospace Telegram Bot (Python port)

A line-for-line Python port of the original Go implementation, using
[python-telegram-bot](https://python-telegram-bot.org) (PTB) — the most
widely used and actively developed Python Telegram Bot library — and the
Python standard library's `sqlite3` for statistics storage.

Converts any text you send — plus captions on photos, videos, voice notes,
and other media — into Telegram monospace formatting. You choose how the
text is chunked before each chunk is wrapped in its own monospace span:

- **Word** — each word is individually monospaced.
- **Sentence** — each sentence is individually monospaced.
- **Paragraph** — each paragraph is individually monospaced.
- **Full** — the entire message is monospaced as one block.

Original spacing, line breaks, and content are preserved. If the result
exceeds Telegram's message length limit, it's automatically split into
multiple messages, preferring to break at paragraph, then sentence, then
word, then character boundaries.

The bot also keeps lightweight usage statistics (active users, message
counts over several time windows) backed by SQLite, viewable in-chat.

## ⚡ One-click deploy: the one file you need to edit

**Before deploying, open [`deploy_config.py`](./deploy_config.py) at the
repository root and replace the placeholder `BOT_TOKEN` with a real token
from [@BotFather](https://t.me/BotFather).** Every other file is ready to
go as-is — nothing else needs to change for a Railway deployment.
`deploy_config.py` is a plain Python file with three constants and
extensive comments explaining each one; environment variables (if you set
them instead, e.g. in Railway's dashboard) always take priority over the
constants in that file, so you can use either approach. If you deploy
without editing this file, the bot fails fast on startup with a clear
message telling you what to fix, rather than starting up broken.

**Security note:** if you fill in a real token and this repository is or
might become public, use the Railway environment variable instead of
editing `deploy_config.py` — a token committed to a public repo is a
public token.

## Usage

Start a chat with the bot and use the persistent keyboard:

- **Start** — shows a welcome message.
- **Settings** — choose your active mode (Word, Sentence, Paragraph, Full)
  or view **📊 Statistics**.

Once a mode is set, just send text or media with a caption, and the bot
replies with the converted version.

## Project structure

Organized by feature area into four packages, each a proper Python
package (`__init__.py` included). Within each package, every function
still lives in its own file, named after what it does — matching the
original Go implementation's one-file-per-function convention, just
grouped by feature instead of sitting flat in one directory.

```
monospace-telegram-bot-python/
├── main.py                          entry point — wires everything together
├── deploy_config.py                 ← EDIT THIS: your BOT_TOKEN (see above)
├── requirements.txt                 runtime dependencies
├── requirements-dev.txt             + pytest, ruff (for tests/CI)
├── pyproject.toml                   ruff + pytest configuration
├── Dockerfile
├── README.md
├── .github/workflows/ci.yml         CI: lint, format check, tests, Docker build
│
├── tests/                           unit tests — no network/Telegram dependency
│   ├── conftest.py                  makes the repo root importable
│   ├── test_core.py                 Mode round-trip, config fallback logic
│   ├── test_rendering.py            splitting/wrapping/rendering logic
│   └── test_stats.py                stats tracking + the Feb-29 leap-year fix
│
├── core/                            domain types shared by every other package
│   ├── __init__.py
│   ├── config.py                    loads BOT_TOKEN / PORT / RAILWAY_PUBLIC_DOMAIN (env, with deploy_config.py fallback)
│   ├── mode.py                      Mode enum + DEFAULT_MODE
│   ├── mode_label.py                Mode -> button label
│   ├── mode_parse.py                button label -> Mode
│   └── limits.py                    Telegram message/caption length limits
│
├── rendering/                       pure text transformation — no Telegram dependency
│   ├── __init__.py
│   ├── render.py                    render(): text -> monospaced text, by mode
│   ├── render_units.py              wraps each split unit in its own code span
│   ├── wrap_code.py                 wraps a string in a Telegram code span
│   ├── split_surrounding_space.py   separates leading/trailing whitespace
│   ├── split_words.py               splits text into words
│   ├── split_sentences.py           splits text into sentences
│   ├── split_paragraphs.py          splits text into paragraphs
│   ├── closing_mark.py              recognizes trailing quote/bracket marks
│   ├── split_for_telegram.py        splits long output into multiple messages
│   ├── best_split_point.py          picks the best boundary to cut at
│   ├── last_word_break.py           finds the last whitespace break
│   ├── last_sentence_break.py       finds the last sentence break
│   └── last_index_after.py          finds the index just after a substring
│
├── telegram_ui/                     bot-facing layer — menus, handlers, media, webhook
│   ├── __init__.py
│   ├── new_bot.py                   constructs the PTB Application instance
│   ├── webhook_url.py               builds the public webhook URL
│   ├── store.py                     per-user mode storage (in memory, asyncio-safe)
│   ├── welcome_text.py              the /start welcome message
│   ├── main_menu.py                 builds the Start/Settings keyboard
│   ├── settings_menu.py             builds the Word/Sentence/Paragraph/Full/Stats keyboard
│   ├── mode_handler.py              handler factory for mode-select buttons
│   ├── register_main_menu_handlers.py  wires /start, Start, Settings, Back
│   ├── register_settings_handlers.py   wires the four mode buttons
│   ├── register_content_handlers.py    wires incoming text + media
│   ├── send_rendered.py             sends rendered text, chunked to fit
│   ├── handle_media.py              re-sends media with rendered caption
│   └── resend_media.py              re-sends a message's media by type (via file_id)
│
└── stats/                           SQLite-backed usage statistics
    ├── __init__.py
    ├── db.py                        opens the sqlite3 connection (db.DB), points at /data/stats.db
    ├── db_schema.py                 creates the users/messages tables + indexes
    ├── track_message.py             records one message event + upserts user last_seen
    ├── track_middleware.py          PTB group -1 handler that tracks every update
    ├── stats.py                     Stats dataclass — fields shown on the Statistics page
    ├── load_stats.py                queries SQLite for a fresh Stats snapshot
    ├── format_stats.py              renders a Stats snapshot as the message text (HTML)
    ├── stats_menu.py                builds the inline Refresh keyboard
    ├── register_stats_handlers.py   wires the Statistics button + Refresh button
    └── is_not_modified_err.py       detects Telegram's harmless "not modified" edit error
```

Import direction flows one way: `telegram_ui` and `stats` both depend on
`core` and (for `telegram_ui`) `rendering`, but `core` and `rendering`
never import from `telegram_ui` or `stats` — so the pure logic stays
usable (and testable) completely independently of the Telegram library.

## Requirements

- Python 3.10+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Porting notes (Go → Python)

A few places don't translate 1:1 and are worth knowing about:

- **Webhook serving**: telebot.v3 runs its own HTTP listener via a
  `Webhook` poller. PTB's `Application.run_webhook(...)` does the same
  job natively (it starts its own `tornado`-based server) — no separate
  Flask/FastAPI app is needed. Installing PTB with the `[webhooks]` extra
  (already in `requirements.txt`) is required for this to work.
- **Middleware**: telebot's `bot.Use(trackMiddleware)` runs one function
  ahead of every handler. PTB has no direct equivalent; the idiomatic PTB
  mechanism is a `TypeHandler` registered in an earlier **handler group**
  (group `-1`, ahead of the default group `0`) — PTB processes groups
  independently, so this handler runs for every update regardless of
  which other handler also matches it. See `stats/track_middleware.py`.
- **Button binding**: telebot binds handlers to button *objects* by
  identity (`bot.Handle(&btn, ...)`). PTB's `ReplyKeyboardMarkup` buttons
  are just text — handlers are matched with
  `MessageHandler(filters.Text([label]), ...)`. Handler **registration
  order matters**: exact-text handlers are registered before the generic
  text-catch-all in `telegram_ui/register_content_handlers.py`, so they win first,
  mirroring telebot's behavior.
- **Media re-sending**: both versions re-send the original file rather
  than re-uploading it, using Telegram's `file_id`.
- **SQLite concurrency**: the Go version explicitly caps
  `SetMaxOpenConns(1)` to serialize writes. PTB runs its event loop on a
  single thread by default, so all handler coroutines (including the
  synchronous `sqlite3` calls here) execute one at a time on that thread
  — the same effective guarantee, achieved differently.
- **Year-in-time-window math**: Go's `time.AddDate(-1, 0, 0)` silently
  rolls Feb 29 forward to Mar 1 in a non-leap target year. Python's
  `datetime.replace(year=...)` raises `ValueError` in that exact case —
  `stats/load_stats.py` includes a small helper (`_minus_one_year`) that
  reproduces Go's rollover behavior instead of crashing once a year.

## Statistics storage

Usage statistics are stored in a SQLite database at `/data/stats.db`,
using the Python standard library's `sqlite3` module — no extra
dependency needed.

Two tables are created automatically on first run:

- `users` — one row per Telegram user, tracking `first_seen`/`last_seen`.
- `messages` — one row per tracked update, used to compute counts over
  various time windows.

Every incoming update (text, caption, media, sticker, document, etc.) is
recorded via a bot-wide tracking handler (see `stats/track_middleware.py`), so
no individual handler needs to be edited to stay counted.

The Statistics page shows: active users (last 5 minutes), unique users
(all-time), and message counts for today, the trailing 24 hours, 7 days,
30 days, 1 year, and lifetime.

## Configuration

| Variable                 | Description                                                              |
| ------------------------- | -------------------------------------------------------------------------- |
| `BOT_TOKEN`               | Your Telegram bot token. Falls back to `deploy_config.py` if unset.      |
| `PORT`                    | Port the webhook server listens on. Falls back to `deploy_config.py` (default `8080`) if unset. |
| `RAILWAY_PUBLIC_DOMAIN`   | Public domain Telegram sends webhook updates to (no scheme). Falls back to `deploy_config.py` if unset. |

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Either export environment variables:
export BOT_TOKEN=your-telegram-bot-token
export RAILWAY_PUBLIC_DOMAIN=your-public-domain   # e.g. via a tunnel like ngrok

# ...or just edit deploy_config.py and skip the exports above.

python main.py
```

On first run this creates `stats.db` (WAL mode) at whatever `DB_PATH` in
`stats/db.py` points to — see [Deploying on Railway](#deploying-on-railway)
below for persisting it in production.

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

All 22 tests in `tests/` run with no network access and no Telegram bot
token — they cover the rendering pipeline (including Unicode/multi-byte
edge cases), the stats tracking and time-window math (including the
Feb-29 leap-year fix), and the `deploy_config.py` fallback logic in
`core/config.py`. These were executed and verified passing as part of
building this repository, not just written and assumed correct.

`ruff check .` and `ruff format --check .` lint and format-check the
whole repository the same way CI does.

## Deploying on Railway

1. Edit `deploy_config.py` with your bot token (or plan to set
   `BOT_TOKEN` as a Railway environment variable instead).
2. Push this repository to GitHub.
3. Create a new project on Railway and connect your repository. Railway
   will detect the `Dockerfile` and build from it automatically.
4. If you didn't edit `deploy_config.py`, add a `BOT_TOKEN` environment
   variable in the service settings. `RAILWAY_PUBLIC_DOMAIN` and `PORT`
   are provided by Railway automatically.
5. **Add a Volume** to your service and mount it at `/data`. This keeps
   `stats.db` (and therefore your usage statistics) across deploys —
   without it, Railway's container filesystem is wiped on every deploy
   and stats will reset.
6. Deploy. The bot will register its webhook, create the stats tables if
   needed, and start receiving updates.

## Building with Docker

```bash
docker build -t monospace-bot-py .
docker run -e BOT_TOKEN=your-telegram-bot-token \
  -e RAILWAY_PUBLIC_DOMAIN=your-public-domain \
  -v monospace-bot-data:/data \
  -p 8080:8080 monospace-bot-py
```

## CI/CD

`.github/workflows/ci.yml` runs on every push and pull request to `main`:

1. `ruff check .` — lint, run against Python 3.10 and 3.12 in a matrix.
2. `ruff format --check .` — formatting.
3. `pytest tests/ -v` — the 22 unit tests described above.
4. A Docker build of the full deploy image (not pushed anywhere — just
   validates the `Dockerfile` builds cleanly).

There is deliberately no auto-deploy step: Railway's own GitHub
integration (connect the repo in the Railway dashboard) handles
deployment on every push to `main` once you've done that one-time setup,
so CI here focuses purely on catching lint/test/build failures before
they reach that point.

## Notes

- Modes are stored in memory per user and reset if the process restarts.
- Statistics are stored in SQLite on disk and survive process restarts;
  only a fresh deploy without a mounted volume resets them.
- Stickers and video notes are re-sent as-is (they carry no caption in
  the Telegram Bot API, so there is nothing to convert).
- Unsupported message types are politely reported back to the user.
- Tapping Refresh twice in quick succession on an unchanged Statistics
  message is handled gracefully (Telegram's "message is not modified"
  error is caught and treated as a no-op, not a failure).
- This port was written and reviewed without a live Telegram bot token or
  network access to install `python-telegram-bot` in the environment it
  was built in. The pure-logic modules (rendering, splitting, stats
  math) were executed and verified directly; the Telegram-facing layer
  (menus, handlers, webhook wiring) was written carefully against PTB's
  documented v22 API but has not been run against a live bot. Test it
  end-to-end with a real `BOT_TOKEN` before relying on it in production.
