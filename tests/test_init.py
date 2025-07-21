import zettings


def test_import():
    assert zettings.Settings is not None
    assert hasattr(zettings, "__all__")
    assert "Settings" in zettings.__all__
