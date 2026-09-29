"""Central runtime configuration, sourced from environment variables.

Keeping these in one place means CI and local runs can point the suite at a
different base URL or toggle headless mode without touching test code.
"""

import os


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    HEADLESS: bool = os.getenv("HEADLESS", "true").strip().lower() not in ("false", "0", "no")
    DEFAULT_TIMEOUT_MS: int = int(os.getenv("DEFAULT_TIMEOUT_MS", "10000"))
    SLOW_MO_MS: int = int(os.getenv("SLOW_MO_MS", "0"))
