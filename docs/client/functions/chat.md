# 💬 ChatModule

[⬅️ Back to Functions](index.md)

> All methods require authentication (`@require_auth`).  
> Methods marked with `†` also require a logged-in user ID (`@require_uid`).

---

## get_joined_chats

Get chats the current user has joined.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatsList`

```python
# Async
chats = await client.get_joined_chats(circleId="abc")

# Sync
chats = client.get_joined_chats()
```

---

## get_invited_chats

Get chats the current user has been invited to.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatsList`

```python
# Async
invited = await client.get_invited_chats()

# Sync
invited = client.get_invited_chats()
```

---

## get_unread_chats

Get chats that have unread messages.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `UnreadChats`

```python
# Async
unread = await client.get_unread_chats()

# Sync
unread = client.get_unread_chats()
```

---

## get_circle_chats

Get public chats in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatsList`

```python
# Async
chats = await client.get_circle_chats(circleId="abc")

# Sync
chats = client.get_circle_chats(circleId="abc")
```

---

## get_user_hosted_chats

Get chats hosted by a specific user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `userId` | `str` | required | User ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatsList`

```python
# Async
chats = await client.get_user_hosted_chats(userId="xyz")

# Sync
chats = client.get_user_hosted_chats(userId="xyz")
```

---

## get_chat_info

Get details of a specific chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `Chat`

```python
# Async
chat = await client.get_chat_info(chatId="abc")

# Sync
chat = client.get_chat_info(chatId="abc")
```

---

## get_direct_chat

Get an existing DM chat with a user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `userId` | `str` | required | User ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `Chat`

```python
# Async
chat = await client.get_direct_chat(userId="xyz")

# Sync
chat = client.get_direct_chat(userId="xyz")
```

---

## get_chat_messages

Get messages in a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `25` | Number of messages |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatMessageList`

```python
# Async
messages = await client.get_chat_messages(chatId="abc", size=50)

# Sync
messages = client.get_chat_messages(chatId="abc")
```

---

## get_message_info

Get details of a specific message.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `messageId` | `str` | required | Message ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `ChatMessage`

```python
# Async
msg = await client.get_message_info(messageId="msg-id")

# Sync
msg = client.get_message_info(messageId="msg-id")
```

---

## send_message `†`

Send a text message to a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `content` | `str` | required | Message text |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `reply_message_id` | `str \| None` | `None` | Message ID to reply to |

**Returns:** `ChatMessage`

```python
# Async
msg = await client.send_message(chatId="abc", content="Hello!")

# Sync
msg = client.send_message(chatId="abc", content="Hello!", reply_message_id="msg-id")
```

---

## send_photo `†`

Send an image message to a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `image` | `IO \| BufferedReader` | required | Image file |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `reply_message_id` | `str \| None` | `None` | Message ID to reply to |

**Returns:** `ChatMessage`

```python
# Async
with open("photo.jpg", "rb") as f:
    await client.send_photo(chatId="abc", image=f)

# Sync
with open("photo.jpg", "rb") as f:
    client.send_photo(chatId="abc", image=f)
```

---

## send_sticker_message `†`

Send a sticker message.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `stickerId` | `str` | required | Sticker ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `reply_message_id` | `str \| None` | `None` | Message ID to reply to |

**Returns:** `ChatMessage`

```python
# Async
await client.send_sticker_message(chatId="abc", stickerId="sticker-id")

# Sync
client.send_sticker_message(chatId="abc", stickerId="sticker-id")
```

---

## send_chat_entity `†`

Send a raw chat entity. Use this for custom message types.

| Parameter | Type | Description |
|---|---|---|
| `chatId` | `str` | Chat ID |
| `entity` | `dict` | Message payload dict |
| `message_type` | `int` | Message type. See `ChatMessageTypes`. |
| `circleId` | `str \| None` | Circle ID (global if omitted) |

**Returns:** `ChatMessage`

```python
# Async
await client.send_chat_entity(chatId="abc", entity={"content": "Hi"}, message_type=ChatMessageTypes.Text)

# Sync
client.send_chat_entity(chatId="abc", entity={"content": "Hi"}, message_type=ChatMessageTypes.Text)
```

---

## delete_message

Delete a message.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `messageId` | `str` | required | Message ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.delete_message(messageId="msg-id")

# Sync
client.delete_message(messageId="msg-id")
```

---

## mark_as_read_chat

Mark a chat as read.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.mark_as_read_chat(chatId="abc")

# Sync
client.mark_as_read_chat(chatId="abc")
```

---

## start_direct_chat

Start a direct message chat with a user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `userId` | `str` | required | User ID to DM |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `message` | `str \| None` | `None` | Optional opening message |

**Returns:** `tuple[Chat, ChatMessageList]`

```python
# Async
chat, messages = await client.start_direct_chat(userId="xyz", message="Hey!")

# Sync
chat, messages = client.start_direct_chat(userId="xyz")
```

---

## start_group_chat

Create a group chat with multiple users.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `userIds` | `list` | required | List of user IDs to invite |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `tuple[Chat, ChatMessageList]`

```python
# Async
chat, messages = await client.start_group_chat(userIds=["uid1", "uid2"])

# Sync
chat, messages = client.start_group_chat(userIds=["uid1", "uid2"])
```

---

## start_public_chat

Create a public chat in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `image` | `IO \| BufferedReader` | required | Chat icon image |
| `title` | `str` | required | Chat title |
| `content` | `str \| None` | `None` | Chat description |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `tuple[Chat, ChatMessageList]`

```python
# Async
with open("icon.png", "rb") as f:
    chat, messages = await client.start_public_chat(image=f, title="My Chat")

# Sync
with open("icon.png", "rb") as f:
    chat, messages = client.start_public_chat(image=f, title="My Chat", content="Welcome!")
```

---

## join_chat

Join a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `Chat`

```python
# Async
await client.join_chat(chatId="abc")

# Sync
client.join_chat(chatId="abc")
```

---

## leave_chat

Leave a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `Chat`

```python
# Async
await client.leave_chat(chatId="abc")

# Sync
client.leave_chat(chatId="abc")
```

---

## invite_to_chat

Invite one or more users to a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `userIds` | `str \| list` | required | Single user ID or list of IDs |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.invite_to_chat(chatId="abc", userIds=["uid1", "uid2"])

# Sync
client.invite_to_chat(chatId="abc", userIds="uid1")
```

---

## kick

Kick a user from a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `userId` | `str` | required | User ID to kick |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.kick(chatId="abc", userId="xyz")

# Sync
client.kick(chatId="abc", userId="xyz")
```

---

## unkick

Unkick a previously kicked user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `userId` | `str` | required | User ID to unkick |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.unkick(chatId="abc", userId="xyz")

# Sync
client.unkick(chatId="abc", userId="xyz")
```

---

## mute_chat

Mute or unmute a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `isMuted` | `bool` | `True` | `True` to mute, `False` to unmute |

**Returns:** `ChatMember`

```python
# Async
await client.mute_chat(chatId="abc", isMuted=True)

# Sync
client.mute_chat(chatId="abc", isMuted=False)
```

---

## set_chat_read_only

Set a chat to read-only mode.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `isReadOnly` | `bool` | `True` | `True` to enable, `False` to disable |

**Returns:** `Chat`

```python
# Async
await client.set_chat_read_only(chatId="abc")

# Sync
client.set_chat_read_only(chatId="abc", isReadOnly=False)
```

---

## edit_chat

Edit chat name, description, or icon.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `name` | `str \| None` | `None` | New chat name |
| `content` | `str \| None` | `None` | New description |
| `icon` | `IO \| BufferedReader \| None` | `None` | New icon image |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `Chat`

```python
# Async
await client.edit_chat(chatId="abc", name="New Name")

# Sync
with open("icon.png", "rb") as f:
    client.edit_chat(chatId="abc", icon=f, content="Updated desc")
```

---

## enable_chat / disable_chat

Enable or disable a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `note` | `str \| None` | `None` | Optional note |

**Returns:** `Chat`

```python
# Async
await client.enable_chat(chatId="abc")
await client.disable_chat(chatId="abc", note="Maintenance")

# Sync
client.disable_chat(chatId="abc")
```

---

## add_chat_cohost / remove_chat_cohost

Add or remove a co-host in a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `userIds` | `str \| list` | required | User ID(s) — `add` only |
| `userId` | `str` | required | User ID — `remove` only |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.add_chat_cohost(chatId="abc", userIds=["uid1"])
await client.remove_chat_cohost(chatId="abc", userId="uid1")

# Sync
client.add_chat_cohost(chatId="abc", userIds="uid1")
```

---

## transfer_chat_host

Transfer the host role to another user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `userId` | `str` | required | New host's user ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.transfer_chat_host(chatId="abc", userId="xyz")

# Sync
client.transfer_chat_host(chatId="abc", userId="xyz")
```

---

## equip_chat_persona

Equip a persona for the current user in a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `personaId` | `str` | required | Persona ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `ChatMember`

```python
# Async
await client.equip_chat_persona(chatId="abc", personaId="persona-id")

# Sync
client.equip_chat_persona(chatId="abc", personaId="persona-id")
```

---

## set_chat_wallpaper

Set a wallpaper image for a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `image` | `IO \| BufferedReader` | required | Wallpaper image file |
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `Chat`

```python
# Async
with open("bg.jpg", "rb") as f:
    await client.set_chat_wallpaper(image=f, chatId="abc")

# Sync
with open("bg.jpg", "rb") as f:
    client.set_chat_wallpaper(image=f, chatId="abc")
```

---

## set_chat_bubble

Set a chat bubble style for a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `bubbleId` | `str` | `"none"` | Bubble ID, or `"none"` to remove |
| `useAsDefault` | `bool` | `False` | Apply as default for the chat |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.set_chat_bubble(chatId="abc", bubbleId="bubble-id")

# Sync
client.set_chat_bubble(chatId="abc", bubbleId="none")
```

---

## get_my_sticker_packs

Get sticker packs owned by the current user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `20` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `StickerPackList`

```python
# Async
packs = await client.get_my_sticker_packs()

# Sync
packs = client.get_my_sticker_packs()
```

---

## get_stickers

Get stickers in a specific pack.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `packId` | `str` | required | Sticker pack ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `50` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `StickerList`

```python
# Async
stickers = await client.get_stickers(packId="pack-id")

# Sync
stickers = client.get_stickers(packId="pack-id")
```

---

## save_sticker

Save an image as a sticker in a pack.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `packId` | `str` | required | Sticker pack ID |
| `image` | `IO \| BufferedReader` | required | Sticker image file |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `StickerInfo`

```python
# Async
with open("sticker.png", "rb") as f:
    sticker = await client.save_sticker(packId="pack-id", image=f)

# Sync
with open("sticker.png", "rb") as f:
    sticker = client.save_sticker(packId="pack-id", image=f)
```

---

[⬅️ Back to Functions](index.md)