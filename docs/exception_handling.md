# 🚨 Exception Handling

In the Kyodo library, all errors are divided into two categories:

1. **`LibraryError`** — errors related to incorrect usage of the library (invalid arguments, missing data, etc.).
2. **`KyodoError`** — errors related to the server or API restrictions (denials, access issues, rate limits, etc.).

All exceptions inherit from the base class **`Exception`**.  
The full list of exceptions can be found in the source code: [exceptions.py](https://github.com/alx0rr/kyodo/blob/main/kyodo/utils/exceptions.py)

---

## 🔹 Basic Usage

```python
from kyodo import exceptions

try:
    # Your code calling Kyodo API
    ...
except exceptions.NeedAuthError:
    # Handle cases where authorization is required
    print("Authorization is required!")
except exceptions.UnsupportedArgumentType:
    # Handle unsupported argument types
    print("Unsupported argument type!")
except exceptions.KyodoError as e:
    # Catch all other Kyodo server errors
    print(f"Kyodo error occurred: {e}")
except exceptions.LibraryError as e:
    # Catch all library-related errors
    print(f"Library error occurred: {e}")
except Exception as e:
    # Catch any other Python errors
    print(f"Unknown error: {e}")
```

---

## 🔹 Examples

### Example 1 — Authorization error

```python
from kyodo import exceptions

try:
    client.send_message(circleId, chatId, "Hello!")
except exceptions.NeedAuthError:
    print("You must log in before sending messages.")
```

### Example 2 — General case

```python
from kyodo import exceptions

try:
    client.login()
except exceptions.KyodoError as e:
    print(f"Server-side error: {e}")
except exceptions.LibraryError as e:
    print(f"Library error: {e}")
```

---

## 🔗 Navigation

[⬅️ Main page](index.md) | [Next section: Objects](objects.md)
