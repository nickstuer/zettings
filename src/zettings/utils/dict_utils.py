from typing import Annotated, Any

from beartype import beartype
from beartype.vale import Is

from zettings.exceptions import KeyNotFoundError, MappingError
from zettings.utils.validation_utils import is_valid_key


@beartype
def get_dotted_key(
    d: dict,
    key: Annotated[str, Is[lambda s: is_valid_key(s)]],
) -> Any:  # noqa: ANN401
    """Get a value from a dictionary using a dotted key notation.

    Args:
        d (dict): The dictionary to search.
        key (str): The key to retrieve the value for.

    Returns:
        Any: The value associated with the key.

    Raises:
        KeyNotFoundError: If the key is not found in the dictionary.

    """
    for k in key.split("."):
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            raise KeyNotFoundError(key)

    return d


@beartype
def set_dotted_key(
    d: dict,
    key: Annotated[str, Is[lambda s: is_valid_key(s)]],
    value: Annotated[Any, Is[lambda v: v is not None]],  # noqa: ANN401
) -> None:
    """Set a value from a dictionary using a dotted key notation.

    Args:
        d (dict): The dictionary to modify.
        key (str): The key to set the value for.
        value (Any): The value to set.

    Raises:
        MappingError: If the key points to a non dictionary value.

    """
    keys = key.split(".")

    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        if not isinstance(d[k], dict):
            raise MappingError(k)
        d = d[k]

    d[keys[-1]] = value


@beartype
def del_dotted_key(
    d: dict,
    key: Annotated[str, Is[lambda s: is_valid_key(s)]],
) -> None:
    """Delete a dotted key from a dictionary.

    Args:
        d (dict): The dictionary to modify.
        key (str): The key to delete.

    Raises:
        KeyNotFoundError: If the key is not found in the dictionary.
        MappingError: If the key points to a non dictionary value.

    """
    keys = key.split(".")

    for k in keys[:-1]:
        if k not in d:
            raise KeyNotFoundError(key)
        if not isinstance(d[k], dict):
            raise MappingError(k)
        d = d[k]

    if keys[-1] not in d:
        raise KeyNotFoundError(key)
    del d[keys[-1]]
