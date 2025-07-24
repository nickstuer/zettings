"""Decorator utilities for the Zettings library.

This module provides decorator functions that enhance type safety and error
handling throughout the Zettings library. The primary decorator converts
beartype validation errors into custom Zettings exceptions for consistent
error handling across the entire library.
"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

from beartype.roar import BeartypeHintViolation

from zettings.exceptions import TypeHintError

__all__ = ["beartype_wrapper"]

P = ParamSpec("P")
T = TypeVar("T")


def beartype_wrapper(func: Callable[P, T]) -> Callable[P, T]:
    """Wrap a function to convert BeartypeHintViolation to TypeHintError.

    This decorator catches beartype validation errors and converts them to
    the custom TypeHintError for consistent error handling throughout the
    Zettings library.

    Args:
        func: The function to wrap with beartype error handling.

    Returns:
        The wrapped function that converts beartype errors.

    Raises:
        TypeHintError: When the wrapped function raises BeartypeHintViolation.

    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except BeartypeHintViolation as cause:
            raise TypeHintError(str(cause)) from cause

    return wrapper
