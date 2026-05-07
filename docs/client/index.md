# 📡 Client Reference

[⬅️ Back to main](../index.md)

Both `AsyncClient` and `Client` expose **identical methods** — the only difference is that async methods require `await`.

## 🔄 Choosing a Client

| | `AsyncClient` | `Client` (Sync) |
|---|---|---|
| **Import** | `from kyodo import AsyncClient` | `from kyodo import Client` |
| **Use with** | `asyncio`, `async def` | regular scripts, bots |
| **Method calls** | `await client.method()` | `client.method()` |
| **socket_trace** | ✗ | ✓ |
| **socket_daemon** | ✗ | ✓ |

---

## 📦 Initialization

```python
# Async
from kyodo import AsyncClient

client = AsyncClient(
    deviceId="your-device-id",
    language="en",
    region="en",
    timezone="Europe/Oslo",
    socket_enable=True,
    proxy=None
)

# Sync
from kyodo import Client

client = Client(
    deviceId="your-device-id",
    language="en",
    region="en",
    timezone="Europe/Oslo",
    socket_enable=True,
    socket_trace=False,   # sync only
    socket_daemon=True,   # sync only
    proxy=None
)
```

## ⚙️ Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `deviceId` | `str \| None` | `None` | Unique device identifier. If not provided, one is generated automatically. **It is strongly recommended to always use the same value** to avoid session and authentication issues. |
| `language` | `str` | `"en"` | Language code for API requests and responses. See supported values via `client.get_supported_languages()`. |
| `region` | `str` | `"en"` | API region for routing requests. Examples: `"eu"`, `"us"`, `"ru"`, `"asia"`. |
| `user_agent` | `str` | `"okhttp/4.12.0"` | User-Agent header sent with HTTP requests. |
| `timezone` | `str` | `"Europe/Oslo"` | IANA timezone identifier. Affects how the server interprets timestamps. Examples: `"Europe/Oslo"`, `"Asia/Tokyo"`. |
| `socket_enable` | `bool` | `True` | Enables WebSocket support for real-time events (messages, updates, etc.). |
| `socket_trace` | `bool` | `False` | *(Sync only)* Enables low-level socket debug logging. Logs connect, send, receive, and close events. Recommended for development only. |
| `socket_daemon` | `bool` | `True` | *(Sync only)* If `True`, socket threads won't block application shutdown. Set to `False` for long-running services that need clean shutdown. |
| `proxy` | `ProxyConfig \| ProxyPool \| None` | `None` | Proxy for all outgoing connections. See [Proxy Configuration](#-proxy-configuration) below. |

---

## 🧩 Attributes & Objects

| Name | Type | Description |
|---|---|---|
| `client.me` | `kyodo.UserProfile` | Currently authenticated user profile. Available after login. |
| `client.account` | `kyodo.AccountInfo` | Currently authenticated account information. Available after login. |
| `client.req` | `kyodo.Requester` | Internal HTTP request handler. |
| `client.socket_enable` | `bool` | Whether WebSocket support is enabled. |
| `client.language` | `str` | Language code in use. |
| `client.region` | `str` | Region in use. |
| `client.user_agent` | `str` | User-Agent string in use. |
| `client.timezone` | `str` | Timezone in use. |
| `client.token` | `str` | Current session token. Available after login. |
| `client.deviceId` | `str` | Device identifier. |
| `client.userId` | `str \| None` | Authenticated user ID. Available after login. |

---

## 🌐 Proxy Configuration

Proxy support applies to both HTTP and WebSocket connections.

**Supported types:** `HTTP`, `SOCKS4`, `SOCKS5`

```python
from kyodo.objects.args import ProxyConfig, ProxyPool, ProxyType, ProxyUsage

# Single proxy
proxy = ProxyConfig(host="1.2.3.4", port=1080, proxy_type=ProxyType.SOCKS5)

# From URL
proxy = ProxyConfig.from_url("socks5://user:pass@1.2.3.4:1080")

# Proxy pool (random proxy is picked per request)
pool = ProxyPool()
pool.add(ProxyConfig.from_url("http://1.2.3.4:8080"))
pool.add(ProxyConfig.from_url("socks5://1.2.3.4:1080"))

# Usage flags — control where proxy is applied
ProxyConfig.from_url("http://1.2.3.4:8080",   usage=ProxyUsage.HTTP)  # HTTP only
ProxyConfig.from_url("socks5://1.2.3.4:1080", usage=ProxyUsage.WS)   # WebSocket only
ProxyConfig.from_url("socks5://1.2.3.4:1080", usage=ProxyUsage.ALL)  # everywhere (default)
```

### Changing proxy at runtime

```python
client.set_proxy(ProxyConfig.from_url("socks5://1.2.3.4:1080")) #or ProxyPool

# Remove proxy
client.set_proxy(None)

# Read current proxy
print(client.proxy)
```

---

## 🔌 WebSocket

```python
# Async
await client.ws_connect()
await client.ws_disconnect()
await client.close()  # alias for ws_disconnect

# Sync
client.ws_connect()
client.ws_disconnect()
client.close()  # alias for ws_disconnect
```

---

## 🖨️ String Representation

```python
str(client)
# Async:  "kyodo.AsyncClient <deviceId=abc123, socket_enable=True>"
# Sync:   "kyodo.Client <deviceId=abc123, socket_enable=True>"

repr(client)
# Full representation with all parameters
```
---

## 📚 Function Modules
 
All client methods are organized by module. Click a module to see its full function list with parameters.
 
| Module | Description |
|---|---|
| [🔐 AuthModule](functions/auth.md) | Login, register, token management, email verification |
| [🌐 CommonModule](functions/common.md) | Notifications, search, store, topics, share links |
| [💬 ChatModule](functions/chat.md) | Messages, chats, stickers, co-hosts |
| [👤 UserModule](functions/user.md) | Profiles, follows, blocks, badges, online status |
| [🔵 CircleModule](functions/circle.md) | Circles, explore, leaderboards |
| [🛡️ CircleAdminModule](functions/circle_admin.md) | Moderation: ban, strike, warn, join requests |
| [📝 BlogModule](functions/blog.md) | Posts, comments, personas, wikis |
| [🔌 WebSocket](websocket.md) | Real-time events, typing, commands, middleware |
 
> **[→ Full function index with all methods](functions/index.md)**


---

## 🔗 Navigation
[⬅️ Main page](../index.md) | [Next section: Exception Handling](../exception_handling.md)