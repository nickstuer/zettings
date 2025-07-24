# Zettings

![PyPI](https://img.shields.io/pypi/v/zettings?label=zettings)
![Python Versions](https://img.shields.io/badge/python-3.10+-blue?logo=python)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/zettings)](https://pypistats.org/packages/zettings)
[![GitHub issues](https://img.shields.io/github/issues/nickstuer/zettings.svg)](https://github.com/nickstuer/zettings/issues)

![Lines Of Code](https://tokei.rs/b1/github/nickstuer/zettings)
[![Codecov](https://img.shields.io/codecov/c/github/nickstuer/zettings)](https://app.codecov.io/gh/nickstuer/zettings)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nickstuer/zettings/run_tests.yml)](https://github.com/nickstuer/zettings/actions/workflows/run_tests.yml)

[![license](https://img.shields.io/github/license/nickstuer/zettings.svg)](LICENSE)

A settings management library that exposes project settings as standard Python dictionaries with TOML file persistence.

**Zettings** is a Python settings library designed for simplicity and developer experience. It implements the MutableMapping protocol to expose settings as standard Python dictionaries while providing persistent storage to TOML files with advanced features like auto_reload, read_only mode, thread safety, and dotted key notation for nested settings.


## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Example](#basic-example)
  - [Advanced Features](#advanced-features)
  - [Settings Options](#settings-options)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Features

**Modern & Type-Safe**
- **TOML Support**: Uses TOML format for modern, readable settings files
- **Type Safety**: Comprehensive type hints and runtime validation with beartype
- **MutableMapping Protocol**: Full compatibility with Python's dictionary interface

**Developer Experience**
- **Auto Reload**: Automatically reload settings from file when accessed
- **Thread Safety**: Locking for concurrent access
- **Default Values**: Provide default values for settings to aid with fallback values
- **Defaults Sync**: Automatically writes default settings to the file if the file is missing default keys

**Advanced Features**
- **Dotted Key Notation**: Access nested settings with `"parent.child.key"` syntax
- **Read-only Mode**: Protect settings from accidental modifications
- **RAM-only Mode**: In memory settings without file persistence
- **File Paths**: Specify exact TOML file path for Zettings to use
- **Metadata Tracking**: Automatic creation and update timestamps

## Quick Start

```python
from zettings import Zettings

# Create settings with defaults
defaults = {
    "database.host": "192.168.0.1",
    "database.port": 69,
    "theme.dark": True
}
settings = Zettings("myapp", defaults)

# Use like a regular dictionary
print(settings["database.host"])  # "192.168.0.1"
settings["database.host"] = "localhost"
```

## Installation

### Using pip
```bash
pip install zettings
```

### Using uv (recommended)
```bash
uv pip install zettings
```

### Requirements
- Python 3.10 or higher
- Dependencies: `toml`, `beartype`

## Usage

### Basic Example

```python
from zettings import Zettings

# Initialize with a name (creates ~/.myapp/settings.toml)
settings = Zettings("myapp")

# Set values using dictionary syntax
settings["name"] = "John Doe"
settings["preferences.theme"] = "dark"
settings["preferences.notifications"] = True

# Access values using dictionary syntax
username = settings["username"]  # "John Doe"
theme = settings["preferences.theme"]  # "dark"

# Fallback values
timeout = settings.get("api.timeout", 30)  # 30 if not set
```

### Advanced Features

#### Dotted Key Notation
Access nested settings with dot notation:

```python
# Zettings approach:
settings["database.connection.host"] = "localhost"

# Standard nested dictionary approach would be:
if "database" not in settings:
    settings["database"] = {}
if "connection" not in settings["database"]:
    settings["database"]["connection"] = {}
settings["database"]["connection"]["host"] = "localhost"
```

#### Default Values
Provide default settings for your application:

```python
defaults = {
    "server": {
        "host": "localhost",
        "port": 6969,
        "debug": False
    },
    "theme": {
        "color": "blue",
        "dark": True
    }
}

settings = Zettings("myapp", defaults)
```

#### Provide File Path for Zettings
```python
from pathlib import Path
from zettings import Zettings

path = Path("C:/myapp/settings.toml")
settings = Zettings("myapp", filepath=path)
```

### Zettings Options

```python
settings = Zettings(
    name="myapp",                    # App name (used for default file path)
    defaults=None,                   # Default values dictionary
    filepath=None,                   # Custom TOML file path
    ram_only=False,                  # Memory-only mode (no file persistence)
    auto_reload=True,                # Auto-reload file on each access
    read_only=False,                 # Prevent modifications
    save_metadata=True               # Include creation/update timestamps
)
```

## API Reference

### Zettings Class

#### Constructor Parameters
- **`name`** (str): Application name for default file path generation
- **`defaults`** (dict, optional): Default settings values
- **`filepath`** (Path, optional): Custom path to TOML file
- **`ram_only`** (bool): If True, settings exist only in memory
- **`auto_reload`** (bool): Automatically reload file on access
- **`read_only`** (bool): Prevent write operations
- **`save_metadata`** (bool): Include metadata in TOML file

#### Methods
- **`get(key, fallback=None)`**: Get value with optional fallback
- **`set(key, value)`**: Set settings value
- **`exists(key)`**: Check if key exists in settings
- **`__getitem__(key)`**: Dictionary style access
- **`__setitem__(key, value)`**: Dictionary style assignment
- **`__delitem__(key)`**: Delete settings key

#### Properties
- **`filepath`**: Path to the TOML settings file
- **`name`**: Application name
- **`read_only`**: Whether settings are read-only

### Exceptions
- **`ZettingsError`**: Base exception class
- **`InvalidKeyError`**: Invalid settings key format
- **`KeyNotFoundError`**: Settings key not found
- **`ReadOnlyError`**: Attempt to modify read-only settings
- **`InvalidValueError`**: Invalid settings value
- **`TypeHintError`**: Type validation error

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

### Guidelines
- Add type hints to all new code
- Include tests for new features
- Update documentation as needed

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nickstuer/zettings.git
   cd zettings
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

### Bug Reports and Feature Requests
Please use the [issue tracker](https://github.com/nickstuer/zettings/issues) to report bugs or request new features.

### Contributors

<a href="https://github.com/nickstuer/zettings/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=nickstuer/zettings"/>
</a>

## License

[MIT © Nick Stuer](LICENSE)
