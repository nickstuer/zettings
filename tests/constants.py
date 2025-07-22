NAME = "test_settings"

DEFAULTS_NORMAL = {
    "key1": "value1",
    "key2": "value2",
    "key3": {"subkey1": "subvalue1", "subkey2": "subvalue2", "subkey3": {"subsubkey1": "subsubvalue1"}},
    "key4": ["listitem1", "listitem2", "listitem3"],
    "key5": {"subkey1": ["listitem1", "listitem2", "listitem3"], "subkey2": "subvalue2"},
    "key6": "value6",
    "key7": {"subkey1": "subvalue1", "subkey2": "subvalue2", "subkey3": {"subsubkey1": "subsubvalue1"}},
    "key8": True,
    "key9": 69,
    "key10": 3.14,
}

DEFAULTS_NESTED = {
    "key1": "value1",
    "key2": "value2",
    "key3.subkey1": "subvalue1",
    "key3.subkey2": "subvalue2",
    "key3.subkey3.subsubkey1": "subsubvalue1",
    "key4": ["listitem1", "listitem2", "listitem3"],
    "key5.subkey1": ["listitem1", "listitem2", "listitem3"],
    "key5.subkey2": "subvalue2",
    "key6": "value6",
    "key7.subkey1": "subvalue1",
    "key7.subkey2": "subvalue2",
    "key7.subkey3.subsubkey1": "subsubvalue1",
    "key8": True,
    "key9": 69,
    "key10": 3.14,
}
