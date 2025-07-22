from zettings.exceptions import (
    InvalidKeyError,
    InvalidValueError,
    KeyNotFoundError,
    MappingError,
    ReadOnlyError,
    TypeHintError,
    ZettingsError,
)


def test_zettings_errors_inherit_zettings_error():
    assert issubclass(InvalidKeyError, ZettingsError)
    assert issubclass(KeyNotFoundError, ZettingsError)
    assert issubclass(MappingError, ZettingsError)
    assert issubclass(ReadOnlyError, ZettingsError)
    assert issubclass(InvalidValueError, ZettingsError)
    assert issubclass(TypeHintError, ZettingsError)


def test_zettings_error_inherits_base_exception():
    assert issubclass(ZettingsError, Exception)
