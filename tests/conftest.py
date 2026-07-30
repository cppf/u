"""Shared pytest configuration: makes the repo root importable so tests
can `import core`, `import rendering`, `import stats`, `import
telegram_ui` without installing the project as a package.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
