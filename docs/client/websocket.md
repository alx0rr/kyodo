# 🔌 WebSocket

Real-time communication via WebSocket. Available on both `AsyncClient` and `Client`.

[⬅️ Back to Functions](functions/index.md)

---

## Connecting

```python
# Async
await client.ws_connect()
await client.ws_disconnect()

# Sync
client.ws_connect()
client.ws_disconnect()
```

> WebSocket connects automatically if `socket_enable=True` (default) after login.

---

## ws_send

Send raw data over the WebSocket connection.

| Parameter | Type | Description |
|---|---|---|
| `data` | `str \| dict \| bytes` | Data to send. Dicts are serialized to JSON automatically. |

```python
# Async
await client.ws_send({"o": "some_event", "d": {"key": "value"}})

# Sync
client.ws_send({"o": "some_event", "d": {"key": "value"}})
```

---

## ws_typing

Send a typing indicator in a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | ID of the chat |
| `circleId` | `str \| None` | `None` | Circle ID, if the chat belongs to a circle |

```python
# Async
await client.ws_typing(chatId="chat-id", circleId="circle-id")

# Sync
client.ws_typing(chatId="chat-id", circleId="circle-id")
```

---

## ws_typing_end

Stop the typing indicator in a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | ID of the chat |
| `circleId` | `str \| None` | `None` | Circle ID, if the chat belongs to a circle |

```python
# Async
await client.ws_typing_end(chatId="chat-id", circleId="circle-id")

# Sync
client.ws_typing_end(chatId="chat-id", circleId="circle-id")
```

---

## ws_open_circle_screen

Notify the server that the user opened a circle screen.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | ID of the circle |

```python
# Async
await client.ws_open_circle_screen(circleId="circle-id")

# Sync
client.ws_open_circle_screen(circleId="circle-id")
```

---

## ws_close_circle_screen

Notify the server that the user closed a circle screen.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | ID of the circle |

```python
# Async
await client.ws_close_circle_screen(circleId="circle-id")

# Sync
client.ws_close_circle_screen(circleId="circle-id")
```

---

## Event Handling

Use decorators to register handlers for incoming WebSocket events.

### Registering an event handler

```python
from kyodo import EventType

@client.event(EventType.ChatMessage)
def on_message(data):
    print(data.content)
```

### Handling any event

```python
@client.event(EventType.ANY)
def on_any(data):
    print(data)
```

### Registering a command

Commands match the beginning of incoming text messages.

```python
@client.command(["/help", "!help"])
async def on_help(data):
    await client.send_message(chatId=data.chatId, text="Help is on the way!")
```

> ℹ️ `data.content` is automatically stripped of the command prefix before being passed to the handler.

### Middleware

Middlewares run before event handlers. Return `False` to stop the event from reaching handlers.

```python
@client.middleware(EventType.ChatMessage)
def filter_bots(data):
    if data.author.userId == client.userId:
        return False  # stop processing
```


---



# event types

Event types define which kind of event is handled by middleware and event handlers.
All available event types are defined in the EventType class.

Each event type corresponds to a specific action or message received from the server.
Event types are used when registering:

- event handlers

- middleware

### Importing EventType
```python
from kyodo import EventType
```

### 📋 Available Event Types


| EventType | Type | Description |
|-----------|------|-------------|
| `ANY` | `str` | Matches any incoming event |
| `ChatMessage` | `int` | Any chat message |
| `DeleteMessage` | `int` | Message deletion |
| `ChatTextMessage` | `str` | Text message |
| `ChatImageMessage` | `str` | Image message |
| `ChatStickerMessage` | `str` | Sticker message |
| `ChatMemberJoin` | `str` | User joined the chat |
| `ChatMemberLeave` | `str` | User left the chat |
| `VoiceChatStarted` | `str` | Voice chat started |
| `VoiceChatEnded` | `str` | Voice chat ended |
| `OpenChatScreen` | `int` | Chat screen opened |
| `Ping` | `int` | Server ping |
| `Notification` | `int` | System notification |
| `...` | `...` | ... |


### 📌 Notes
- You can see a list of all event types in the [source code](https://github.com/alx0rr/kyodo/blob/main/kyodo/objects/args/event_type.py)

- ANY can be used to catch all events

- string-based event types represent subtypes of base events

- a single handler can be registered for multiple event types

- the same event types are used by both middleware and event handlers


# сonnection lifecycle

The WebSocket connection runs in a separate asyncio task.  
If the main coroutine finishes, the event loop stops and the connection is closed with an error.

To prevent this, **you must call `socket_wait()` at the end of your program**.  
This keeps the process alive and prevents the socket from being closed.

### Example

```python


client.login()
client.socket_wait()

#async

async def main():
    await client.login()
    await client.socket_wait()
```

### Graceful shutdown

To exit without errors, explicitly close the client before terminating the application:

```python

client.close()

#async
await client.close()

```

Calling `client.close()` properly shuts down the WebSocket connection.



[⬅️ Back to Functions](functions/index.md)