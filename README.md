# zettings

![PyPI](https://img.shields.io/pypi/v/zettings?label=zettings)
![Python Versions](https://img.shields.io/badge/python-3.9+-blue?logo=python)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/zettings)](https://pypistats.org/packages/zettings)
[![GitHub issues](https://img.shields.io/github/issues/nickstuer/zettings.svg)](https://github.com/nickstuer/zettings/issues)

![Lines Of Code](https://tokei.rs/b1/github/nickstuer/zettings)
[![Codecov](https://img.shields.io/codecov/c/github/nickstuer/zettings)](https://app.codecov.io/gh/nickstuer/zettings)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nickstuer/zettings/run_tests.yml)](https://github.com/nickstuer/zettings/actions/workflows/run_tests.yml)

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![license](https://img.shields.io/github/license/nickstuer/zettings.svg)](LICENSE)

A lightweight, TOML-backed configuration/settings utility that that exposes project settings as standard Python dictionaries.

zettings is a Python configuration library designed for simplicity and developer ergonomics. It loads settings data from TOML files and exposes them as standard Python dictionaries — allowing you to work with settings in a familiar, Pythonic way.

## Table of Contents

- [Features](https://github.com/nickstuer/zettings?tab=readme-ov-file#features)
- [Install](https://github.com/nickstuer/zettings?tab=readme-ov-file#install)
- [Usage](https://github.com/nickstuer/zettings?tab=readme-ov-file#usage)
- [Contributing](https://github.com/nickstuer/zettings?tab=readme-ov-file#contributing)
- [License](https://github.com/nickstuer/zettings?tab=readme-ov-file#license)

## Features

- TOML-powered: Uses TOML under the hood for modern, human-friendly settings files.
- Dictionary-like interface: Access and manipulate settings with regular dictionary operations.
- Nested access: Supports nested keys with dotted key notation.
- Optional `defaults`: Provide default values for initializing the settings file or for when a key is missing in the settings file.
- Optional `always_reload`: Reload the setting file everytime a key is read. (Enabled by default)
- Optional `filepath`: Provide the exact file Path of the .toml file to use. (overrides name)


## Install

```
# PyPI
pip install zettings
```
or
```
uv add zettings
```

## Dependencies
Python 3.9 or greater

## Usage

### Example
This will create/use a 'settings.toml' file located in the '.zettings' directory of the user's home directory.
```python
from zettings import Settings

# Standard Dictionary Format
defaults = {
    "settings": {
        "name": "MyName",
        "mood": "happy",
    },
}
# Dotted Key Notation
defaults = {}
defaults["settings.name"] = "MyName"
defaults["settings.mood"] = "happy"

settings = Settings(".zettings/settings.toml", defaults) # Change 'zettings' to your project's name

print(settings["settings.mood"])
settings["settings.mood"] = "angry"
print(settings["settings.mood"])
```
## Contributing

PRs accepted.

If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

#### Bug Reports and Feature Requests
Please use the [issue tracker](https://github.com/nickstuer/zettings/issues) to report any bugs or request new features.

#### Contributors

<a href = "https://github.com/nickstuer/zettings/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=nickstuer/zettings"/>
</a>

## License

[MIT © Nick Stuer](LICENSE)