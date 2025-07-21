from zettings.exceptions import (
    InvalidKeyFormatError,
    KeyNotADictionaryError,
    KeyNotFoundError,
    ReadOnlyError,
    ZettingsError,
)


def test_zettings_errors_inherit_zettings_error():
    assert issubclass(InvalidKeyFormatError, ZettingsError)
    assert issubclass(KeyNotFoundError, ZettingsError)
    assert issubclass(KeyNotADictionaryError, ZettingsError)
    assert issubclass(ReadOnlyError, ZettingsError)


def test_zettings_error_inherits_base_exception():
    assert issubclass(ZettingsError, Exception)
