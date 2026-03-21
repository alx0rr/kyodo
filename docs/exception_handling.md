# Exception Handling

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


## Exception Attributes

All Kyodo exceptions provide additional attributes
that allow you to access detailed error information and the HTTP response.

Available attributes:

- message: str | None
  Error message returned by the API or lib

- response: AsyncHTTPResponse | None
  Original HTTP response object

- request: HTTPRequest | None
  Original HTTP request object

These attributes are available in all exceptions inherited from
LibraryError and KyodoError. (Most often, classes inheriting LibraryError will not have an AsyncHTTPResponse object.)


## Accessing error details

Example — handling an unknown error
```python
from kyodo import exceptions
try:
    await client.login("EMAIL", "PASSWORD")
except exceptions.UnknownError as error:
    print(error.message)

    if error.response:
        print("HTTP status:", error.response.status)
    if error.request:
        print("URL: ", error.request.url)

```

## 🔹 Request & Response Data Objects

Kyodo internally uses two objects to **structure request and response data**.  
These objects are **not meant for direct usage**, but their attributes are available via exceptions (`LibraryError` and `KyodoError`):

- **`HTTPRequest`** — stores the details of the original request.  
- **`AsyncHTTPResponse`** — stores the details of the server response along with the original request.

### HTTPRequest Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `method` | `str` | HTTP method of the request (e.g., `"GET"`, `"POST"`) |
| `url` | `str` | Full URL of the request |
| `body` | `str \| dict \| bytes \| None` | Request body payload |
| `headers` | `dict \| None` | Request headers |
| `proxy` | `str \| dict \| None` | Proxy used for the request |

### AsyncHTTPResponse Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `status` | `int` | HTTP status code (e.g., 200, 404) |
| `_body` | `bytes` | Raw response body (use `text()` / `json()` for decoding) |
| `headers` | `dict` | Response headers |
| `url` | `str` | URL of the request |
| `method` | `str` | HTTP method of the request |
| `encoding` | `str` | Character encoding used for decoding the body |
| `request` | `HTTPRequest` | Original request object |

### Notes

Methods like text() and json() can be used to decode the response body:

```python
if error.response:
    body_str = await e.response.text()
    body_json = await e.response.json()
```

---

## 🔗 Navigation

[⬅️ Main page](index.md) | [Next section: Objects](objects.md)
