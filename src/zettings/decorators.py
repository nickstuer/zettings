from functools import wraps
from typing import Any

from beartype.roar import BeartypeHintViolation

from zettings.exceptions import TypeHintError


def beartype_wrapper(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        try:
            return func(*args, **kwargs)
        except BeartypeHintViolation as cause:
            raise TypeHintError(cause) from cause

    return wrapper
