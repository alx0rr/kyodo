# 🔐 AuthModule

[⬅️ Back to Functions](index.md)

---

## login

Login with email and password.

| Parameter | Type | Description |
|---|---|---|
| `email` | `str` | Account email address |
| `password` | `str` | Account password |

**Returns:** `UserProfile`

```python
# Async
profile = await client.login(email="user@example.com", password="secret")

# Sync
profile = client.login(email="user@example.com", password="secret")
```

---

## login_token

Login using an existing session token.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `token` | `str` | required | Session token |
| `refresh_token` | `bool` | `False` | Whether to refresh the token on login |

**Returns:** `UserProfile`

```python
# Async
profile = await client.login_token(token="your-token")

# Sync
profile = client.login_token(token="your-token")
```

---

## logout

Log out of the current session.

**Returns:** `Any`

```python
# Async
await client.logout()

# Sync
client.logout()
```

---

## register

Register a new account.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `email` | `str` | required | Email address |
| `password` | `str` | required | Password |
| `username` | `str` | required | Username |
| `turnstileToken` | `str` | required | Cloudflare Turnstile verification token |
| `birthday` | `str` | `"Sun Apr 04 2004 02:00:00 GMT+0200"` | Birthday string |

**Returns:** `UserProfile`

```python
# Async
profile = await client.register(
    email="user@example.com",
    password="secret",
    username="myusername",
    turnstileToken="cf-token"
)

# Sync
profile = client.register(
    email="user@example.com",
    password="secret",
    username="myusername",
    turnstileToken="cf-token"
)
```

---

## refresh_token

Refresh the current session token.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `token` | `str \| None` | `None` | Token to refresh. Uses current session token if not provided. |

**Returns:** `UserProfile`

```python
# Async
profile = await client.refresh_token()

# Sync
profile = client.refresh_token()
```

---

## check_age

Check age eligibility by birthday string.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `birthday` | `str` | `"Sun Apr 04 2004 02:00:00 GMT+0200"` | Birthday in JS Date string format |

**Returns:** `BirthdayInfo`

```python
# Async
info = await client.check_age(birthday="Sun Jan 01 2000 00:00:00 GMT+0000")

# Sync
info = client.check_age(birthday="Sun Jan 01 2000 00:00:00 GMT+0000")
```

---

## email_available_check

Check whether an email address is available for registration.

| Parameter | Type | Description |
|---|---|---|
| `email` | `str` | Email address to check |

**Returns:** `bool`

```python
# Async
available = await client.email_available_check(email="user@example.com")

# Sync
available = client.email_available_check(email="user@example.com")
```

---

## username_available_check

Check whether a username is available for registration.

| Parameter | Type | Description |
|---|---|---|
| `username` | `str` | Username to check |

**Returns:** `bool`

```python
# Async
available = await client.username_available_check(username="myusername")

# Sync
available = client.username_available_check(username="myusername")
```

---

## request_email_verification_code

Request an email verification code to be sent to the given address.

| Parameter | Type | Description |
|---|---|---|
| `email` | `str` | Target email address |

**Returns:** `Any`

```python
# Async
await client.request_email_verification_code(email="user@example.com")

# Sync
client.request_email_verification_code(email="user@example.com")
```

---

## email_verification

Verify an email address using a code.

| Parameter | Type | Description |
|---|---|---|
| `email` | `str` | Email address to verify |
| `code` | `int` | Verification code received by email |

**Returns:** `Any`

```python
# Async
await client.email_verification(email="user@example.com", code=123456)

# Sync
client.email_verification(email="user@example.com", code=123456)
```

---

## request_reset_password_code

Request a password reset code to be sent by email.

| Parameter | Type | Description |
|---|---|---|
| `email` | `str` | Email address linked to the account |

**Returns:** `Any`

```python
# Async
await client.request_reset_password_code(email="user@example.com")

# Sync
client.request_reset_password_code(email="user@example.com")
```

---

## reset_password

Reset the account password using a code.

| Parameter | Type | Description |
|---|---|---|
| `email` | `str` | Email address linked to the account |
| `code` | `int` | Reset code received by email |

**Returns:** `Any`

```python
# Async
await client.reset_password(email="user@example.com", code=123456)

# Sync
client.reset_password(email="user@example.com", code=123456)
```

---

## change_password

Change the current account password.

> ⚠️ Full parameters not yet documented.

---

## delete_account

Delete the current account permanently.

> ⚠️ Full parameters not yet documented.

---

[⬅️ Back to Functions](index.md)