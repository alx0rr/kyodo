# 📝 BlogModule

[⬅️ Back to Functions](index.md)

> All methods require authentication (`@require_auth`).

---

## get_kyodo_team_posts

Get official posts from the Kyodo team.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
posts = await client.get_kyodo_team_posts()

# Sync
posts = client.get_kyodo_team_posts(size=10)
```

---

## get_recent_posts

Get the most recent posts in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
posts = await client.get_recent_posts(circleId="abc")

# Sync
posts = client.get_recent_posts(circleId="abc", size=50)
```

---

## get_pinned_posts

Get pinned posts in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `int` | `100` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
pinned = await client.get_pinned_posts(circleId="abc")

# Sync
pinned = client.get_pinned_posts(circleId="abc")
```

---

## get_featured_posts

Get featured posts in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
posts = await client.get_featured_posts(circleId="abc")

# Sync
posts = client.get_featured_posts(circleId="abc")
```

---

## get_circle_wikis

Get wiki posts in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
wikis = await client.get_circle_wikis(circleId="abc")

# Sync
wikis = client.get_circle_wikis(circleId="abc")
```

---

## get_user_wikis

Get wiki posts created by a user in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | User ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
wikis = await client.get_user_wikis(circleId="abc", userId="xyz")

# Sync
wikis = client.get_user_wikis(circleId="abc", userId="xyz")
```

---

## get_user_posts

Get posts created by a user in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | User ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
posts = await client.get_user_posts(circleId="abc", userId="xyz")

# Sync
posts = client.get_user_posts(circleId="abc", userId="xyz")
```

---

## get_post_info

Get details of a specific post.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `postId` | `str` | Post ID |

**Returns:** `Blog`

```python
# Async
post = await client.get_post_info(circleId="abc", postId="post-id")

# Sync
post = client.get_post_info(circleId="abc", postId="post-id")
```

---

## get_post_comments

Get comments (threaded replies) on a post.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `postId` | `str` | required | Post ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PostList`

```python
# Async
comments = await client.get_post_comments(circleId="abc", postId="post-id")

# Sync
comments = client.get_post_comments(circleId="abc", postId="post-id")
```

---

## toggle_post_like

Like or unlike a post (toggles current state).

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `postId` | `str` | Post ID |

**Returns:** `Blog`

```python
# Async
post = await client.toggle_post_like(circleId="abc", postId="post-id")

# Sync
post = client.toggle_post_like(circleId="abc", postId="post-id")
```

---

## delete_post

Delete a post.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `postId` | `str` | Post ID to delete |

```python
# Async
await client.delete_post(circleId="abc", postId="post-id")

# Sync
client.delete_post(circleId="abc", postId="post-id")
```

---

## get_user_personas

Get personas created by a user in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `userId` | `str` | required | User ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PersonaList`

```python
# Async
personas = await client.get_user_personas(circleId="abc", userId="xyz")

# Sync
personas = client.get_user_personas(circleId="abc", userId="xyz")
```

---

## get_my_personas

Get the current user's personas in a circle.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `circleId` | `str` | required | Circle ID |
| `size` | `int` | `25` | Number of results |
| `pageToken` | `str \| None` | `None` | Pagination token |

**Returns:** `PersonaList`

```python
# Async
personas = await client.get_my_personas(circleId="abc")

# Sync
personas = client.get_my_personas(circleId="abc")
```

---

## get_persona_info

Get details of a specific persona.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `personaId` | `str` | Persona ID |

**Returns:** `Persona`

```python
# Async
persona = await client.get_persona_info(circleId="abc", personaId="persona-id")

# Sync
persona = client.get_persona_info(circleId="abc", personaId="persona-id")
```

---

## delete_persona

Delete a persona.

| Parameter | Type | Description |
|---|---|---|
| `circleId` | `str` | Circle ID |
| `personaId` | `str` | Persona ID to delete |

**Returns:** `Persona`

```python
# Async
await client.delete_persona(circleId="abc", personaId="persona-id")

# Sync
client.delete_persona(circleId="abc", personaId="persona-id")
```

---

[⬅️ Back to Functions](index.md)