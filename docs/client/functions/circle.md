# 🔵 CircleModule

[⬅️ Back to Functions](index.md)

> All methods require authentication (`@require_auth`).

---

## get_joined_circles

Get all circles the current user has joined.

**Returns:** `list[Circle]`

```python
# Async
circles = await client.get_joined_circles()

# Sync
circles = client.get_joined_circles()
```

---

## get_unread_circleIds

Get IDs of circles that have unread content.

**Returns:** `list[str]`

```python
# Async
ids = await client.get_unread_circleIds()

# Sync
ids = client.get_unread_circleIds()
```

---

## get_circle_info

Get details of a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |

**Returns:** `CircleInfo`

```python
# Async
info = await client.get_circle_info(circleId="abc")

# Sync
info = client.get_circle_info(circleId="abc")
```

---

## get_circle_description

Get the description text of a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |

**Returns:** `str`

```python
# Async
desc = await client.get_circle_description(circleId="abc")

# Sync
desc = client.get_circle_description(circleId="abc")
```

---

## join_circle

Join a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `invitationId` | `str \| None` | `None` | Invitation ID for private circles |

**Returns:** `CircleInfo`

```python
# Async
await client.join_circle(circleId="abc")

# Sync
client.join_circle(circleId="abc", invitationId="invite-id")
```

---

## leave_circle

Leave a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |

**Returns:** `CircleInfo`

```python
# Async
await client.leave_circle(circleId="abc")

# Sync
client.leave_circle(circleId="abc")
```

---

## request_to_join_circle

Request to join a private circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `message` | `str` | Join request message |

```python
# Async
await client.request_to_join_circle(circleId="abc", message="Hi, I'd like to join!")

# Sync
client.request_to_join_circle(circleId="abc", message="Hi, I'd like to join!")
```

---

## create_circle

Create a new circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | `str` | required | Circle name |
| `image` | `IO \| BufferedReader` | required | Circle icon image |
| `themeColor` | `str` | `"#0090FF"` | Theme color (hex) |
| `isThemeDark` | `bool` | `True` | Dark theme toggle |
| `language` | `str` | `"en"` | Circle language |
| `privacy` | `int` | `CirclePrivacy.Open` | Privacy setting. See `CirclePrivacy`. |
| `templateId` | `int` | `CircleTemplate.FromScratch` | Template. See `CircleTemplate`. |

**Returns:** `CircleInfo`

```python
# Async
with open("icon.png", "rb") as f:
    circle = await client.create_circle(name="My Circle", image=f)

# Sync
with open("icon.png", "rb") as f:
    circle = client.create_circle(name="My Circle", image=f, themeColor="#FF5500")
```

---

## get_explore_page

Get the explore page with circle modules.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `region` | `str \| None` | `None` | Region filter (uses client region if omitted) |

**Returns:** `list[ExploreModule]`

```python
# Async
explore = await client.get_explore_page()

# Sync
explore = client.get_explore_page(region="eu")
```

---

## get_explore_suggested_page

Get suggested circles on the explore page.

**Returns:** `list[Circle]`

```python
# Async
suggested = await client.get_explore_suggested_page()

# Sync
suggested = client.get_explore_suggested_page()
```

---

## get_24h_leaderboard

Get the 24-hour activity leaderboard for a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `str` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `UserProfileList`

```python
# Async
board = await client.get_24h_leaderboard(circleId="abc")

# Sync
board = client.get_24h_leaderboard(circleId="abc", size=10)
```

---

## get_7d_leaderboard

Get the 7-day activity leaderboard for a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `str` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `UserProfileList`

```python
# Async
board = await client.get_7d_leaderboard(circleId="abc")

# Sync
board = client.get_7d_leaderboard(circleId="abc")
```

---

## get_circle_alerts

Get moderation alerts for a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |

**Returns:** `CircleAlerts`

```python
# Async
alerts = await client.get_circle_alerts(circleId="abc")

# Sync
alerts = client.get_circle_alerts(circleId="abc")
```

---

---

# 🛡️ CircleAdminModule

[⬅️ Back to Functions](index.md)

> All methods require authentication (`@require_auth`).  
> These methods are for circle owners and moderators.

---

## get_circle_join_requests

Get pending join requests for a private circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `str` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `JoinRequestList`

```python
# Async
requests = await client.get_circle_join_requests(circleId="abc")

# Sync
requests = client.get_circle_join_requests(circleId="abc")
```

---

## resolve_circle_join_request

Approve or deny a join request.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | Requesting user's ID |
| `isApproved` | `bool` | `True` | `True` to approve, `False` to deny |

```python
# Async
await client.resolve_circle_join_request(circleId="abc", userId="xyz", isApproved=True)

# Sync
client.resolve_circle_join_request(circleId="abc", userId="xyz", isApproved=False)
```

---

## hide_user / unhide_user

Hide or unhide a user in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | User ID |
| `note` | `str \| None` | `None` | Optional moderator note |

**Returns:** `UserProfile`

```python
# Async
await client.hide_user(circleId="abc", userId="xyz", note="Spam")
await client.unhide_user(circleId="abc", userId="xyz")

# Sync
client.hide_user(circleId="abc", userId="xyz")
```

---

## strike_user

Issue a strike (mute) to a user in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | User ID |
| `message` | `str` | required | Strike reason |
| `muteTime` | `str` | `MuteDuration.ONE_HOUR` | Mute duration. See `MuteDuration`. |

```python
# Async
await client.strike_user(circleId="abc", userId="xyz", message="Spamming", muteTime=MuteDuration.ONE_HOUR)

# Sync
client.strike_user(circleId="abc", userId="xyz", message="Breaking rules")
```

---

## revoke_strike_user

Revoke a strike from a user.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | User ID |
| `note` | `str \| None` | `None` | Optional note |

**Returns:** `UserProfile`

```python
# Async
await client.revoke_strike_user(circleId="abc", userId="xyz")

# Sync
client.revoke_strike_user(circleId="abc", userId="xyz", note="Resolved")
```

---

## warn_user

Send a warning to a user.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `userId` | `str` | User ID |
| `message` | `str` | Warning message |

```python
# Async
await client.warn_user(circleId="abc", userId="xyz", message="Please follow the rules.")

# Sync
client.warn_user(circleId="abc", userId="xyz", message="Final warning.")
```

---

## ban_user / unban_user

Ban or unban a user from a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | User ID |
| `message` | `str \| None` | `None` | Optional ban/unban note |

**Returns:** `UserProfile`

```python
# Async
await client.ban_user(circleId="abc", userId="xyz", message="Repeated violations")
await client.unban_user(circleId="abc", userId="xyz")

# Sync
client.ban_user(circleId="abc", userId="xyz")
```

---

## edit_user_titles

Set custom titles for a user in a circle.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `userId` | `str` | User ID |
| `titles` | `list[dict \| UserTitle]` | List of title objects |

Each title is either a `UserTitle` object or a dict with:

| Key | Type | Description |
|---|---|---|
| `text` | `str` | Title label |
| `fg` | `str` | Text color (hex) |
| `bg` | `str` | Background color (hex) |
| `isOfficial` | `bool \| None` | Official badge flag (optional) |

**Returns:** `UserProfile`

```python
from kyodo.objects import UserTitle

# Async
await client.edit_user_titles(
    circleId="abc",
    userId="xyz",
    titles=[UserTitle(text="Moderator", fg="#FFFFFF", bg="#FF0000")]
)

# Sync — dict form also accepted
client.edit_user_titles(
    circleId="abc",
    userId="xyz",
    titles=[{"text": "VIP", "fg": "#FFD700", "bg": "#000000"}]
)
```

---

## delete_circle

Permanently delete a circle. Requires the account password.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `password` | `str` | Account password for confirmation |

**Returns:** `Circle`

```python
# Async
await client.delete_circle(circleId="abc", password="my-password")

# Sync
client.delete_circle(circleId="abc", password="my-password")
```

---

[⬅️ Back to Functions](index.md)