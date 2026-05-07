# 📚 Functions Reference

All methods are available on both `AsyncClient` and `Client`.  
Async versions require `await`. Methods marked with `*` have full signatures documented.

---

## 🔐 [AuthModule](auth.md) — Authentication & Account

| Method | Returns | Description |
|---|---|---|
| [`login`](auth.md#login) `*` | `UserProfile` | Login with email and password |
| [`login_token`](auth.md#login_token) `*` | `UserProfile` | Login with an existing token |
| [`logout`](auth.md#logout) | `Any` | Log out of the current session |
| [`register`](auth.md#register) `*` | `UserProfile` | Register a new account |
| [`refresh_token`](auth.md#refresh_token) `*` | `UserProfile` | Refresh the session token |
| [`check_age`](auth.md#check_age) `*` | `BirthdayInfo` | Check age by birthday string |
| [`email_available_check`](auth.md#email_available_check) `*` | `bool` | Check if email is available |
| [`username_available_check`](auth.md#username_available_check) `*` | `bool` | Check if username is available |
| [`email_verification`](auth.md#email_verification) `*` | `Any` | Verify email with a code |
| [`request_email_verification_code`](auth.md#request_email_verification_code) `*` | `Any` | Request email verification code |
| [`request_reset_password_code`](auth.md#request_reset_password_code) `*` | `Any` | Request password reset code |
| [`reset_password`](auth.md#reset_password) `*` | `Any` | Reset password with code |
| `change_password` | `Any` | Change current password |
| `delete_account` | `Any` | Delete the current account |

---

## 🌐 [CommonModule](common.md) — General API

| Method | Returns | Description |
|---|---|---|
| `get_notifications` | `Any` | Get user notifications |
| `mark_as_read_notifications` | `Any` | Mark notifications as read |
| `get_notices` | `Any` | Get system notices |
| `mark_as_read_notice` | `Any` | Mark a notice as read |
| `get_topics_list` | `Any` | Get list of available topics |
| `get_available_languages` | `Any` | Get supported language list |
| `get_kyodo_events` | `Any` | Get Kyodo platform events |
| `get_link_info` | `Any` | Get info about a share link |
| `get_share_link` | `Any` | Generate a share link |
| `search` | `Any` | Global search |
| `send_report` | `Any` | Send a report |
| `send_active_time` | `Any` | Send active time ping |
| `get_store_items` | `Any` | Get store items |
| `get_store_avatar_frames` | `Any` | Get avatar frames in store |
| `get_store_latest_avatar_frames` | `Any` | Get latest avatar frames |
| `get_store_chat_bubbles` | `Any` | Get chat bubbles in store |
| `get_store_latest_chat_bubbles` | `Any` | Get latest chat bubbles |
| `get_my_avatar_frames` | `Any` | Get owned avatar frames |
| `get_my_chat_bubbles` | `Any` | Get owned chat bubbles |
| `get_audit_log` | `Any` | Get audit log |

---

## 💬 [ChatModule](chat.md) — Chats & Messages

| Method | Returns | Description |
|---|---|---|
| `get_joined_chats` | `Any` | Get list of joined chats |
| `get_invited_chats` | `Any` | Get pending chat invites |
| `get_unread_chats` | `Any` | Get chats with unread messages |
| `get_circle_chats` | `Any` | Get chats in a circle |
| `get_user_hosted_chats` | `Any` | Get chats hosted by a user |
| `get_chat_info` | `Any` | Get chat details |
| `get_direct_chat` | `Any` | Get a DM chat object |
| `get_chat_messages` | `Any` | Get messages in a chat |
| `get_message_info` | `Any` | Get message details |
| `send_message` | `Any` | Send a text message |
| `send_photo` | `Any` | Send a photo message |
| `send_sticker_message` | `Any` | Send a sticker message |
| `send_chat_entity` | `Any` | Send a chat entity |
| `delete_message` | `Any` | Delete a message |
| `mark_as_read_chat` | `Any` | Mark chat as read |
| `start_direct_chat` | `Any` | Start a DM with a user |
| `start_group_chat` | `Any` | Create a group chat |
| `start_public_chat` | `Any` | Create a public chat |
| `edit_chat` | `Any` | Edit chat settings |
| `enable_chat` | `Any` | Enable a chat |
| `disable_chat` | `Any` | Disable a chat |
| `join_chat` | `Any` | Join a chat |
| `leave_chat` | `Any` | Leave a chat |
| `invite_to_chat` | `Any` | Invite a user to chat |
| `kick` | `Any` | Kick a user from chat |
| `unkick` | `Any` | Unkick a user |
| `mute_chat` | `Any` | Mute a chat |
| `set_chat_read_only` | `Any` | Set chat to read-only |
| `set_chat_wallpaper` | `Any` | Set chat wallpaper |
| `set_chat_bubble` | `Any` | Set chat bubble style |
| `add_chat_cohost` | `Any` | Add a co-host to chat |
| `remove_chat_cohost` | `Any` | Remove a co-host |
| `transfer_chat_host` | `Any` | Transfer host role |
| `equip_chat_persona` | `Any` | Equip a persona in chat |
| `get_my_sticker_packs` | `Any` | Get owned sticker packs |
| `get_stickers` | `Any` | Get stickers in a pack |
| `save_sticker` | `Any` | Save a sticker |

---

## 👤 [UserModule](user.md) — User Profiles & Social

| Method | Returns | Description |
|---|---|---|
| `get_user_profile` | `Any` | Get a user's profile |
| `edit_profile` | `Any` | Edit own profile |
| `edit_profile_description` | `Any` | Edit profile description |
| `get_user_followers` | `Any` | Get user followers |
| `get_user_following` | `Any` | Get user following list |
| `toggle_user_following` | `Any` | Follow or unfollow a user |
| `block_user` | `Any` | Block a user |
| `unblock_user` | `Any` | Unblock a user |
| `get_blocked_users` | `Any` | Get list of blocked users |
| `get_user_badges` | `Any` | Get badges of a user |
| `get_online_users` | `Any` | Get online users list |
| `get_online_preview` | `Any` | Get online presence preview |
| `get_chat_users` | `Any` | Get users in a chat |
| `get_circle_users` | `Any` | Get users in a circle |
| `set_online_status` | `Any` | Set own online status |
| `set_avatar_frame` | `Any` | Set avatar frame |
| `pick_topic_tag` | `Any` | Pick a topic tag |
| `unpick_topic_tag` | `Any` | Remove a topic tag |

---

## 🔵 [CircleModule](circle.md) — Circles

| Method | Returns | Description |
|---|---|---|
| `get_circle_info` | `Any` | Get circle details |
| `get_circle_description` | `Any` | Get circle description |
| `get_joined_circles` | `Any` | Get circles the user joined |
| `get_unread_circleIds` | `Any` | Get circles with unread content |
| `get_circle_alerts` | `Any` | Get circle alerts |
| `get_explore_page` | `Any` | Get explore page circles |
| `get_explore_suggested_page` | `Any` | Get suggested circles |
| `get_24h_leaderboard` | `Any` | Get 24h leaderboard |
| `get_7d_leaderboard` | `Any` | Get 7-day leaderboard |
| `create_circle` | `Any` | Create a new circle |
| `join_circle` | `Any` | Join a circle |
| `leave_circle` | `Any` | Leave a circle |
| `request_to_join_circle` | `Any` | Request to join a private circle |

---

## 🛡️ [CircleAdminModule](circle_admin.md) — Circle Moderation

| Method | Returns | Description |
|---|---|---|
| `get_circle_join_requests` | `Any` | Get pending join requests |
| `resolve_circle_join_request` | `Any` | Approve or deny a join request |
| `ban_user` | `Any` | Ban a user from circle |
| `unban_user` | `Any` | Unban a user |
| `hide_user` | `Any` | Hide a user in circle |
| `unhide_user` | `Any` | Unhide a user |
| `strike_user` | `Any` | Issue a strike to a user |
| `revoke_strike_user` | `Any` | Revoke a user's strike |
| `warn_user` | `Any` | Warn a user |
| `edit_user_titles` | `Any` | Edit a user's titles |
| `delete_circle` | `Any` | Delete the circle |

---

## 📝 [BlogModule](blog.md) — Posts & Personas

| Method | Returns | Description |
|---|---|---|
| `get_recent_posts` | `Any` | Get recent posts |
| `get_featured_posts` | `Any` | Get featured posts |
| `get_pinned_posts` | `Any` | Get pinned posts |
| `get_kyodo_team_posts` | `Any` | Get official Kyodo team posts |
| `get_post_info` | `Any` | Get post details |
| `get_post_comments` | `Any` | Get comments on a post |
| `get_user_posts` | `Any` | Get posts by a user |
| `toggle_post_like` | `Any` | Like or unlike a post |
| `delete_post` | `Any` | Delete a post |
| `get_circle_wikis` | `Any` | Get circle wiki pages |
| `get_user_wikis` | `Any` | Get wikis by a user |
| `get_my_personas` | `Any` | Get own personas |
| `get_user_personas` | `Any` | Get personas of a user |
| `get_persona_info` | `Any` | Get persona details |
| `delete_persona` | `Any` | Delete a persona |

---

## 🔌 [WebSocket](../websocket.md) — Real-time & Events

| Method | Returns | Description |
|---|---|---|
| [`ws_connect`](../websocket.md#connecting) | `None` | Connect to WebSocket |
| [`ws_disconnect`](../websocket.md#connecting) | `None` | Disconnect from WebSocket |
| [`ws_send`](../websocket.md#ws_send) `*` | — | Send raw data over WebSocket |
| [`ws_typing`](../websocket.md#ws_typing) `*` | — | Send typing indicator |
| [`ws_typing_end`](../websocket.md#ws_typing_end) `*` | — | Stop typing indicator |
| [`ws_open_circle_screen`](../websocket.md#ws_open_circle_screen) `*` | — | Notify opening circle screen |
| [`ws_close_circle_screen`](../websocket.md#ws_close_circle_screen) `*` | — | Notify closing circle screen |

---

> `*` — full parameters documented on the linked page