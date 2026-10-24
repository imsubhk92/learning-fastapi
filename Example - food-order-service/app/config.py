"""One setting needs only the standard library; no settings framework is needed."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    enable_debug_route: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        """Reject misspelled flags rather than silently enabling a debug feature."""
        value = os.getenv("APP_ENABLE_DEBUG_ROUTE", "false").lower().strip()
        if value not in {"true", "false", "1", "0"}:
            raise ValueError("APP_ENABLE_DEBUG_ROUTE must be true, false, 1, or 0")
        return cls(enable_debug_route=value in {"true", "1"})
