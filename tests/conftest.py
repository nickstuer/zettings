import shutil
from pathlib import Path

import pytest

from tests.constants import NAME
from zettings import Zettings


@pytest.fixture
def temp_filepath(tmpdir_factory: pytest.TempdirFactory):
    temp_dir = str(tmpdir_factory.mktemp("temp"))
    temp_testing_dir = temp_dir + "/testing/settings.toml"
    yield Path(temp_testing_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_homepath():
    temp_homepath = Path.home() / f".{NAME}/settings.toml"
    yield temp_homepath
    if temp_homepath.exists():
        shutil.rmtree(temp_homepath.parent)


@pytest.fixture
def temp_zettings(temp_filepath):
    return Zettings(name=NAME, filepath=temp_filepath, save_metadata=False)
