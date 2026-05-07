# 👤 UserModule

[⬅️ Back to Functions](index.md)

> All methods require authentication (`@require_auth`).

---

## get_user_profile

Get a user's profile in a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `userId` | `str` | User ID |

**Returns:** `UserProfile`

```python
# Async
profile = await client.get_user_profile(circleId="abc", userId="xyz")

# Sync
profile = client.get_user_profile(circleId="abc", userId="xyz")
```

---

## get_blocked_users

Get the list of users blocked by the current account.

**Returns:** `BlockingUsers`

```python
# Async
blocked = await client.get_blocked_users()

# Sync
blocked = client.get_blocked_users()
```

---

## block_user

Block a user.

| Parameter | Type | Description |
|---|---|---|
| `userId` | `str` | ID of the user to block |

**Returns:** `BlockingResult`

```python
# Async
await client.block_user(userId="xyz")

# Sync
client.block_user(userId="xyz")
```

---

## unblock_user

Unblock a user.

| Parameter | Type | Description |
|---|---|---|
| `userId` | `str` | ID of the user to unblock |

**Returns:** `BlockingResult`

```python
# Async
await client.unblock_user(userId="xyz")

# Sync
client.unblock_user(userId="xyz")
```

---

## toggle_user_following

Follow or unfollow a user (toggles the current state).

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `userId` | `str` | User ID |

**Returns:** `UserProfile`

```python
# Async
await client.toggle_user_following(circleId="abc", userId="xyz")

# Sync
client.toggle_user_following(circleId="abc", userId="xyz")
```

---

## get_user_followers

Get the list of users who follow a user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `userId` | `str` | required | User ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `str` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `UserProfileList`

```python
# Async
followers = await client.get_user_followers(userId="xyz", size=25)

# Sync
followers = client.get_user_followers(userId="xyz", size=25)
```

---

## get_user_following

Get the list of users that a user follows.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `userId` | `str` | required | User ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `str` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `UserProfileList`

```python
# Async
following = await client.get_user_following(userId="xyz")

# Sync
following = client.get_user_following(userId="xyz")
```

---

## get_chat_users

Get members of a chat.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `chatId` | `str` | required | Chat ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `type` | `str` | `ChatMemberTypes.All` | Member type filter. See `ChatMemberTypes`. |
| `size` | `int` | `20` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `UserProfileList`

```python
# Async
members = await client.get_chat_users(chatId="abc")

# Sync
members = client.get_chat_users(chatId="abc")
```

---

## get_circle_users

Get members of a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `str` | `25` | Number of results |
| `type` | `str` | `CircleUsersType.Members` | Member type filter. See `CircleUsersType`. |
| `parentId` | `str \| None` | `None` | Parent filter ID |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `UserProfileList`

```python
# Async
members = await client.get_circle_users(circleId="abc")

# Sync
members = client.get_circle_users(circleId="abc")
```

---

## get_online_users

Get online users in a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |

**Returns:** `OnlineUsers`

```python
# Async
online = await client.get_online_users(circleId="abc")

# Sync
online = client.get_online_users(circleId="abc")
```

---

## get_online_preview

Get a preview list of online users in a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |

**Returns:** `list[OnlinePreview]`

```python
# Async
preview = await client.get_online_preview(circleId="abc")

# Sync
preview = client.get_online_preview(circleId="abc")
```

---

## set_online_status

Set the current user's online visibility.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `appearOnline` | `bool` | `True` | Whether to appear online |
| `content` | `str \| None` | `None` | Status text |

**Returns:** `UserProfile`

```python
# Async
await client.set_online_status(appearOnline=True, content="writing bots")

# Sync
client.set_online_status(appearOnline=False)
```

---

## edit_profile

Edit the current user's profile.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `nickname` | `str` | required | Display name |
| `avatar` | `IO \| BufferedReader \| str` | required | Avatar image file or URL |
| `cover` | `IO \| BufferedReader \| str \| None` | required | Cover image file or URL, or `None` to skip |
| `fg` | `str` | `"#FFFFFF"` | Foreground/text color (hex) |
| `bg` | `str` | `"#0F0F0F"` | Background color (hex) |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `UserProfile`

```python
# Async
with open("avatar.jpg", "rb") as f:
    await client.edit_profile(nickname="MyBot", avatar=f, cover=None)

# Sync
with open("avatar.jpg", "rb") as f:
    client.edit_profile(nickname="MyBot", avatar=f, cover=None)
```

---

## edit_profile_description

Edit the current user's bio.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `bio` | `str` | required | New profile description |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `UserProfile`

```python
# Async
await client.edit_profile_description(bio="I am a bot.")

# Sync
client.edit_profile_description(bio="I am a bot.")
```

---

## get_user_badges

Get badges of a user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `userId` | `str` | required | User ID |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `list[UserBadge]`

```python
# Async
badges = await client.get_user_badges(userId="xyz")

# Sync
badges = client.get_user_badges(userId="xyz")
```

---

## set_avatar_frame

Set the avatar frame for the current user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `avatarFrameId` | `str` | `"none"` | Avatar frame ID, or `"none"` to remove |
| `useEverywhere` | `bool` | `False` | Apply to all circles |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `UserProfile`

```python
# Async
await client.set_avatar_frame(avatarFrameId="frame-id", useEverywhere=True)

# Sync
client.set_avatar_frame(avatarFrameId="none")
```

---

## pick_topic_tag

Add a topic tag to the current user's profile.

| Parameter | Type | Description |
|---|---|---|
| `topicId` | `str` | Topic ID to pick |

```python
# Async
await client.pick_topic_tag(topicId="topic-id")

# Sync
client.pick_topic_tag(topicId="topic-id")
```

---

## unpick_topic_tag

Remove a topic tag from the current user's profile.

| Parameter | Type | Description |
|---|---|---|
| `topicId` | `str` | Topic ID to remove |

```python
# Async
await client.unpick_topic_tag(topicId="topic-id")

# Sync
client.unpick_topic_tag(topicId="topic-id")
```

---

[⬅️ Back to Functions](index.md)