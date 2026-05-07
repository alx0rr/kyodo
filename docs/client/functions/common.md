# 🌐 CommonModule

[⬅️ Back to Functions](index.md)

> All methods require authentication (`@require_auth`).

---

## search

Search for circles.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | `str \| None` | `None` | Search query string |
| `region` | `str \| None` | `None` | Region filter (uses client region if omitted) |
| `size` | `int` | `10` | Number of results |

**Returns:** `CircleList`

```python
# Async
results = await client.search(query="gaming", size=20)

# Sync
results = client.search(query="gaming")
```

---

## get_available_languages

Get the list of languages supported by the API.

**Returns:** `AvailableLanguages`

```python
# Async
langs = await client.get_available_languages()

# Sync
langs = client.get_available_languages()
```

---

## get_notifications

Get user notifications.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `NotificationList`

```python
# Async
notifs = await client.get_notifications(size=25)

# Sync
notifs = client.get_notifications()
```

---

## mark_as_read_notifications

Mark notifications as read.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `markAllRead` | `bool` | `True` | Mark all notifications as read |

```python
# Async
await client.mark_as_read_notifications()

# Sync
client.mark_as_read_notifications()
```

---

## get_notices

Get notices in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `NoticeList`

```python
# Async
notices = await client.get_notices(circleId="abc")

# Sync
notices = client.get_notices(circleId="abc")
```

---

## mark_as_read_notice

Mark a notice as read.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `noticeId` | `bool` | `True` | Notice ID |

**Returns:** `Notice`

```python
# Async
await client.mark_as_read_notice(circleId="abc", noticeId="notice-id")

# Sync
client.mark_as_read_notice(circleId="abc", noticeId="notice-id")
```

---

## get_topics_list

Get available topic tags.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | `int` | `25` | Number of results |
| `query` | `str \| None` | `None` | Filter by name |

**Returns:** `list[Topic]`

```python
# Async
topics = await client.get_topics_list(query="anime")

# Sync
topics = client.get_topics_list()
```

---

## get_kyodo_events

Get Kyodo platform events.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | `str` | `KydoEventsType.calendar` | Event type filter |
| `size` | `int` | `50` | Number of results |

**Returns:** `KyodoEventList`

```python
# Async
events = await client.get_kyodo_events()

# Sync
events = client.get_kyodo_events()
```

---

## get_link_info

Resolve a Kyodo share link to get its target object info.

| Parameter | Type | Description |
|---|---|---|
| `link` | `str` | Share link URL |

**Returns:** `ShareLink`

```python
# Async
info = await client.get_link_info(link="https://kyodo.app/...")

# Sync
info = client.get_link_info(link="https://kyodo.app/...")
```

---

## get_share_link

Generate a share link for an object.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `objectId` | `str` | required | ID of the target object |
| `objectType` | `int` | required | Object type. See `KyodoObjectTypes`. |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

**Returns:** `ShareLink`

```python
# Async
link = await client.get_share_link(objectId="abc", objectType=KyodoObjectTypes.User)

# Sync
link = client.get_share_link(objectId="abc", objectType=KyodoObjectTypes.User)
```

---

## send_report

Send a report about a user or object.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `objectId` | `str` | required | ID of the reported object |
| `objectType` | `int` | `KyodoObjectTypes.User` | Object type. See `KyodoObjectTypes`. |
| `reportType` | `int` | `ReportTypes.Other` | Report reason. See `ReportTypes`. |
| `content` | `str \| None` | `None` | Additional comment |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |

```python
# Async
await client.send_report(objectId="xyz", objectType=KyodoObjectTypes.User)

# Sync
client.send_report(objectId="xyz", content="Spam account")
```

---

## send_active_time

Send an active time ping for a circle (keeps presence alive).

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |

```python
# Async
await client.send_active_time(circleId="abc")

# Sync
client.send_active_time(circleId="abc")
```

---

## get_audit_log

Get the audit log for an object.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `objectId` | `str` | required | Object ID |
| `objectType` | `int` | `KyodoObjectTypes.Chat` | Object type. See `KyodoObjectTypes`. |
| `circleId` | `str \| None` | `None` | Circle ID (global if omitted) |
| `size` | `int` | `20` | Number of entries |

**Returns:** `AuditLogList`

```python
# Async
log = await client.get_audit_log(objectId="chat-id")

# Sync
log = client.get_audit_log(objectId="chat-id")
```

---

## get_store_items

Get all items in the store.

**Returns:** `StoreItems`

```python
# Async
store = await client.get_store_items()

# Sync
store = client.get_store_items()
```

---

## get_store_avatar_frames

Get avatar frames available in the store.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | `str \| None` | `None` | Search query |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `AvatarFrameList`

```python
# Async
frames = await client.get_store_avatar_frames(query="golden")

# Sync
frames = client.get_store_avatar_frames()
```

---

## get_store_latest_avatar_frames

Get the latest avatar frames in the store.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `AvatarFrameList`

```python
# Async
frames = await client.get_store_latest_avatar_frames()

# Sync
frames = client.get_store_latest_avatar_frames()
```

---

## get_my_avatar_frames

Get avatar frames owned by the current user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `AvatarFrameList`

```python
# Async
frames = await client.get_my_avatar_frames()

# Sync
frames = client.get_my_avatar_frames()
```

---

## get_store_chat_bubbles

Get chat bubbles available in the store.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | `str \| None` | `None` | Search query |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatBubbleList`

```python
# Async
bubbles = await client.get_store_chat_bubbles()

# Sync
bubbles = client.get_store_chat_bubbles()
```

---

## get_store_latest_chat_bubbles

Get the latest chat bubbles in the store.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatBubbleList`

```python
# Async
bubbles = await client.get_store_latest_chat_bubbles()

# Sync
bubbles = client.get_store_latest_chat_bubbles()
```

---

## get_my_chat_bubbles

Get chat bubbles owned by the current user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `ChatBubbleList`

```python
# Async
bubbles = await client.get_my_chat_bubbles()

# Sync
bubbles = client.get_my_chat_bubbles()
```

---

[⬅️ Back to Functions](index.md)