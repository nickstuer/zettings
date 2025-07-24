"""Constant values for the Zettings library.

This module defines all constant values used throughout the Zettings
settings management library, including metadata keys, default messages,
and validation patterns.
"""

from __future__ import annotations

__all__ = [
    "CREATED_KEY",
    "NAME_PATTERN",
    "NOTICE",
    "NOTICE_KEY",
    "UPDATED_KEY",
]

# Metadata constants for TOML file management
NOTICE_KEY = "metadata.notice"
NOTICE = "This file was created by zettings."
CREATED_KEY = "metadata.created"
UPDATED_KEY = "metadata.updated"

# Validation patterns
NAME_PATTERN = "^[A-Za-z0-9_-]+$"
