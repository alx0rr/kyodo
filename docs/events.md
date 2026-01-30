# Event handling

This section covers events, middleware, and event types used in the Kyodo library.
You will learn how to:

- handle incoming messages and system events via event handlers,

- filter and validate events using middleware,

- use specific event types and subtypes for precise responses to user and server actions.

The section includes examples of registering handlers and middleware, as well as a complete list of available EventType values.

---

## 📌 Page content
- ## [creating bot commands](#commands)
- ## [Event handling](#events)
- ## [Middleware](#middlewares)
- ## [All event types](#event-types)
- ## [Connection lifecycle](#сonnection-lifecycle)
- ## [Main page](index.md)

---


# commands

Commands can be registered in two ways:
by using decorators or by passing a handler function to a dedicated client method.

When a command is processed, the original command trigger is automatically removed.
This means that if a user sends:

```
/say hello
```

the handler will receive only the command arguments:

```
hello
```

### Example

```python
async def echo(message: ChatMessage):
    await client.send_message(
        message.circleId,
        message.chatId,
        message.content,
        message.messageId
    )
client.add_command(["/send"], echo)


@client.command(["/help", "/commands"])
async def help_handler(message: ChatMessage):
    await client.send_message(
        message.circleId,
        message.chatId,
        (
            "Commands list:\n"
            "/help\n"
            "/ping"
        )
    )
```

In this example:

- the /help and /commands commands are registered using a decorator

- the /send command is registered via the add_command method

message.content always contains the command text without the trigger



# events

Event handlers allow you to react to various events occurring within the system.
Each handler is bound to a specific event type defined in the EventType enum.

Depending on the event type, the handler receives an appropriate event payload object.
For example, chat message events provide a ChatMessage object.

Event handlers can be registered in two ways:

- using a decorator

- via a client method

### Registration using a decorator
```python
@client.event(EventType.ChatMessage)
async def hello_handler(message: ChatMessage):
    if message.content.lower() == "hello":
        await client.send_message(
            message.circleId,
            message.chatId,
            "hello my friend",
            message.messageId
        )
```
### Registration via a client method
```python
async def join_handler(message: ChatMessage):
    await client.send_message(
        message.circleId,
        message.chatId,
        f"{message.author.nickname}, welcome to chat"
    )

client.add_handler(EventType.ChatMemberJoin, join_handler)
```
### Event handler characteristics

- each handler is associated with a specific event type

- a single event can have multiple handlers

- handlers receive the original event data without modification

- you can handle any event type, not just chat messages

The full list of available events can be found [here](#event-types).


# middlewares

Middleware are intermediate handlers that are executed before any event handlers or commands.
They are used for preliminary checks, filtering, or modification of incoming data.

For each incoming event, all registered middleware are executed sequentially.
Only after all middleware complete successfully does the system proceed to event and command handling.

If <b> any middleware returns False </b>, the processing is immediately stopped:

- remaining middleware are not executed

- event handlers and commands are not called

- processing of the current socket message is terminated

### Registering middleware using a decorator
```python
@client.middleware(EventType.ChatMessage)
async def user_filter(message: ChatMessage):
    if message.author.userId == client.userId:
        return False
```
In this example, the middleware blocks messages sent by the bot itself.

### Registering middleware via a client method
```python
client.add_middleware(EventType.ChatMessage, user_filter)
```



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
async def main():
    await client.login()
    await client.socket_wait()
```

### Graceful shutdown

To exit without errors, explicitly close the client before terminating the application:

```python
await client.close()
```

Calling `client.close()` properly shuts down the WebSocket connection.



## 🔗 Navigation
[⬅️ Main page](index.md) | [Next section: Exception Handling](exception_handling.md)