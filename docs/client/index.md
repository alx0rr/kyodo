# 🔹 Client Class

The **`Client`** class is the main entry point for interacting with Kyodo servers.  
It provides access to all API features by combining multiple modules and handles user sessions, HTTP requests, and optional socket communication.

---

## Constructor

```python
Client(
    deviceId: str | None = None,
    language: str = "en",
    user_agent: str = "Kyodo/135 CFNetwork/1496.0.7 Darwin/23.5.0",
    timezone: str = "Europe/Oslo",
    socket_enable: bool = True,
    proxy: str | None = None
)
```

### Arguments

- **deviceId** (`str | None`): Unique device identifier. If `None`, a random ID is generated. It is recommended to use a consistent device ID to avoid authentication/session issues.  
- **language** (`str`): Language code used in API requests/responses. Default `'en'`. Examples: `'en'`, `'ru'`, `'ja'`. Supported languages can be listed using `client.get_supported_languages()`.  
- **user_agent** (`str`): User-Agent string sent in HTTP request headers. Defaults to an iOS-style string but can be customized.  
- **timezone** (`str`): Timezone in IANA format (e.g., `"Europe/Oslo"`, `"Asia/Tokyo"`). Affects how timestamps are processed on the server.  
- **socket_enable** (`bool`): Enables real-time socket communication if `True` (e.g., for live messages or updates).  
- **proxy** (`str | None`): Optional proxy URL or None (`http://username:password@127.0.0.1:8080`).


---

## Objects

- **Client.me** (`kyodo.BaseProfile`): The currently authenticated user's profile. Available after login.  
- **Client.req** (`kyodo.Requester`): Internal request handler for HTTP requests.

---

## Attributes & Properties

- **socket_enable** (`bool`): Indicates if socket support is enabled for real-time features  
- **language** (`str`): Current language (`client.language`)  
- **user_agent** (`str`): Current User-Agent string (`client.user_agent`)  
- **timezone** (`str`): Current timezone (`client.timezone`)  
- **token** (`str`): Session token for authorized requests (`client.token`)  
- **deviceId** (`str`): Unique device identifier (`client.deviceId`)  
- **userId** (`str | None`): ID of the currently logged-in user (`client.userId` via `me`)

---

## Example Usage

```python
from kyodo import Client

client = Client(
    deviceId="frZyJ8fi4e4U0KtN61AqHBHeu9",
    socket_enable=False
)
```
### Access profile after login
```python
await client.login("EMAIL", "PASSWORD")
print(client.me.username)
print(client.userId)
print(client.token)
```
### Internal request object (read-only)
```python
print(client.req.language)
print(client.req.deviceId)
```

---

## Notes

- `deviceId` is **important for session consistency**; using different IDs may cause authentication issues  
- `socket_enable` controls real-time features (like live messages)  
- Most objects (`me`, `req`) are **read-only** and meant for internal reference or debugging  
- Properties (`language`, `user_agent`, `timezone`, `token`, `deviceId`, `userId`) provide convenient access without directly using `req` or `me`


## 🔹 Modules Reference

`Client` aggregates functionality from multiple modules. Below is a summary of each module, its purpose, and a link to its source/documentation.

| Module | Purpose | Documentation | Source File |
|--------|---------|---------------|------------|
| **AuthModule** | Login, logout, token management | [AuthModule Docs](kyodo/docs/auth.md) | [auth.py](kyodo/modules/auth.py) |
| **AccountModule** | Account settings, password/email updates, profile management | [AccountModule Docs](kyodo/docs/account.md) | [account.py](kyodo/modules/account.py) |
| **ChatsModule** | Sending and managing chat messages | [ChatsModule Docs](kyodo/docs/chats.md) | [chats.py](kyodo/modules/chats.py) |
| **CirclesModule** | Circle (group) management and interaction | [CirclesModule Docs](kyodo/docs/circles.md) | [circles.py](kyodo/modules/circles.py) |
| **StickersModule** | Sticker management and usage | [StickersModule Docs](kyodo/docs/stickers.md) | [stickers.py](kyodo/modules/stickers.py) |
| **UsersModule** | User-related actions, member lists, blocking | [UsersModule Docs](kyodo/docs/users.md) | [users.py](kyodo/modules/users.py) |
| **CommonModule** | Miscellaneous common-purpose API methods | [CommonModule Docs](kyodo/docs/common.md) | [common.py](kyodo/modules/common.py) |
| **PostsModule** | Managing posts and post folders | [PostsModule Docs](kyodo/docs/posts.md) | [posts.py](kyodo/modules/posts.py) |
| **StoreModule** | Store-related features | [StoreModule Docs](kyodo/docs/store.md) | [store.py](kyodo/modules/store.py) |


---

### Notes

- Each module is **mixed into the Client** class via inheritance, so all their methods are available on `client` instances directly.  
- You can click the links above to see **all functions, parameters, and usage examples** for each module.  
- This table serves as a **quick reference** to understand which module handles which features.





---

## 🔗 Navigation
[⬅️ Main page](../index.md) | [Next section: Event Handling & Command Creation](../events.md)