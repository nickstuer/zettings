import zettings


def test_import():
    assert zettings.Zettings is not None
    assert hasattr(zettings, "__all__")
    assert "Zettings" in zettings.__all__
