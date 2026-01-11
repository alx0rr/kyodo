# 🇬🇧 Logging

Kyodo provides a flexible logging system. You can:

1. Set the **logging level**.  
2. Enable/disable **file logging**.  
3. Use the **built-in `log` object** for convenient message formatting.

Import:

```python
from kyodo import set_log_level, enable_file_logging, disable_file_logging, logging, log
```

---

## 🔹 Set Logging Level

Set the level of logs that should be displayed:

```python
# Set the logging level
set_log_level(logging.INFO)   # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Messages below the specified level will **not be displayed**.

---

## 🔹 File Logging

You can enable or disable logging to a file:

```python
# Enable logging to a file
enable_file_logging('kyodo.log')

# Disable logging to a file
disable_file_logging()
```

- Default file name is `kyodo.log`  
- All messages of the set level or higher are written to the file

---

## 🔹 Built-in `log` Object

Kyodo provides a convenient `log` object for logging messages with a consistent format:

```python
log.debug("Debug message")
log.info("Info message")
log.warning("Warning message")
log.error("Error message")
log.critical("Critical message")
```

### Message Format

The built-in logger formats messages as:

```
"{colored_timestamp} - {colored_level} - {colored_message}"
```

Example:

```
2026-01-11 12:00:00 - INFO - Connected to chat server
```

- `colored_timestamp` — timestamp with highlighting  
- `colored_level` — logging level (INFO, DEBUG, etc.)  
- `colored_message` — the actual log message  

This makes logs **easy to read in the console**.

---

## 🔗 Navigation

[⬅️ Main page](index.md) | [Next section: Examples](examples)
