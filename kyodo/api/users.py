from .base import BaseClass
from ..objects import (
	BaseProfile, MediaTarget, UsersList, CircleRole,
	UserActivity, PersonaInChat, UserPersona, UserPersonasList, MuteDuration
)
from ..utils import require_auth, exceptions, require_uid

from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader

from datetime import UTC
from datetime import datetime as bake



class UsersModule(BaseClass):

	@require_auth
	async def get_kicked_users(self, circleId: str, chatId: str, start: int = 0, limit: int = 15) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/{chatId}/members/kicked?start={start}&limit={limit}")
		return UsersList(await result.json())

	@require_auth
	async def get_banned_users(self, circleId: str, start: int = 0, limit: int = 15) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/users/banned?start={start}&limit={limit}")
		return UsersList(await result.json())

	@require_auth
	async def get_chat_members(self, circleId: str, chatId: str, start: int = 0, limit: int = 100) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/{chatId}/members?start={start}&limit={limit}")
		return UsersList(await result.json())

	@require_auth
	async def get_chat_cohosts(self, circleId: str, chatId: str, start: int = 0, limit: int = 15) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/{chatId}/members/cohosts?start={start}&limit={limit}")
		return UsersList(await result.json())

	@require_auth
	async def get_preview_online_users(self, circleId: str) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/users/online-preview")
		return UsersList(await result.json())

	@require_auth
	async def get_online_users(self, circleId: str, start: int = 0, limit: int = 15) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/users?limit={limit}&start={start}&filter=online")
		return UsersList(await result.json())

	@require_auth
	async def get_circle_users(self, circleId: str, start: int = 0, limit: int = 15, filter: str = "all", role = CircleRole.Member) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/users?limit={limit}&start={start}&role={role or ''}&filter={filter}")
		return UsersList(await result.json())

	@require_auth
	async def get_user_activity(self, userIds: list[str] | str, circleId: str | None = None) -> list[UserActivity]:
		result = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/circles/user-activity/uids", {"targetIds": userIds if isinstance(userIds, list) else [userIds]})
		data: dict = await result.json()
		return [
			UserActivity({"uid": uid, **user})
			for uid, user in data.get("activityMapping", {}).items()
		]


	@require_auth
	async def get_live_layer(self, objectId: str, objectType: int, circleId: str | None = None, limit: int = 3, start: int = 0) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId or "g"}/s/live-layer/page?objectType={objectType}&objectId={objectId}&limit={limit}&start={start}")
		return UsersList(await result.json())
	

	@require_auth
	async def switch_following_status(self, circleId: str, userId: str) -> bool:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/follow/status")
		data: dict = await result.json()
		return bool(data.get("followStatus", 0))


	@require_auth
	async def get_user_followers(self, circleId: str, userId: str, limit: int = 15, start: int = 0) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/users/{userId}/follow/subs/followers?start={start}&limit={limit}")
		return UsersList(await result.json())

	@require_auth
	async def get_user_following(self, circleId: str, userId: str, limit: int = 15, start: int = 0) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/users/{userId}/follow/subs/following?start={start}&limit={limit}")
		return UsersList(await result.json())


	@require_auth
	async def switch_block_user_status(self, userId: str) -> bool:
		result = await self.req.make_async_request("POST", f"/g/s/accounts/blocking/{userId}")
		data: dict = await result.json()
		return data.get("isBlocked")

	@require_auth
	async def get_blocked_users(self, start: int = 0, limit: int = 0) -> UsersList:
		result = await self.req.make_async_request("POST", f"/g/s/accounts/blocking?start={start}&limit={limit}")
		data: dict = await result.json()
		return UsersList({"users": data.get("list", []), "hasMore": data.get("hasMore")})


	@require_auth
	async def get_user_info(self, userId: str, circleId: str | None = None) -> BaseProfile:
		result = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/users/{userId}")
		data: dict = await result.json()
		return BaseProfile(data.get("user"))
	
	@require_auth
	async def get_my_profile(self, circleId: str | None = None) -> BaseProfile:
		return await self.get_user_info('me', circleId)

	@require_auth
	@require_uid
	async def edit_profile(self, circleId: str | None = None, nickname: str | None = None, bio: str | None = None,
			banner: IO | BufferedReader | AsyncBufferedReader | None = None, avatar: IO | BufferedReader | AsyncBufferedReader | None = None) -> BaseProfile:
		data = {}
		if nickname:data["nickname"] = nickname
		if bio:data["bio"] = bio
		if banner:
			banner_data = await self.upload_media(banner, MediaTarget.UserBanner)
			data["banner"]=banner_data.url
		if avatar:
			avatar_data = await self.upload_media(banner, MediaTarget.UserAvatar)
			data["avatar"]=avatar_data.url
		if not data:raise exceptions.NoDataError
		result = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/users/{self.me.userId}", data)
		data = await result.json()
		return BaseProfile(data.get("user"))


	@require_auth
	@require_uid
	async def edit_avatar_frame(self, productId: str | None = None) -> bool:
		await self.req.make_async_request("POST", f"/g/s/users/{self.me.userId}", {
			"avatarFrameId": productId
		})
		return True


	@require_auth
	async def edit_titles(self, circleId: str, userId: str, texts: str | list[str], fontColors: str | list[str] = "#000000", bgColors: str | list[str] = "#FF69B4") -> bool:
		data = {"titles": []}

		texts = texts if isinstance(texts, list) else [texts]
		fontColors = fontColors if isinstance(fontColors, list) else [fontColors]
		bgColors = bgColors if isinstance(bgColors, list) else [bgColors]

		for num, text in enumerate(texts):
			fontColor = fontColors[num] if len(fontColors) > 1 else fontColors[0]
			bgColor = bgColors[num] if len(bgColors) > 1 else bgColors[0]
			data["titles"].append({
				"text": text,
				"fontColor": fontColor,
				"bgColor": bgColor,
				"global": False
			})

		await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/titles", data)
		return True


	@require_auth
	async def get_invitable_members(self, circleId: str, chatId: str | None = None, start: int = 0, limit: int = 15) -> UsersList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/{chatId}/members/invitable?start={start}&limit={limit}")
		return UsersList(await result.json())



	@require_auth
	async def mute_user(self, circleId: str, userId: str, reason: str = "", exp_time: MuteDuration = MuteDuration.ONE_HOUR) -> bool:
		actual_time = bake.now(UTC) + exp_time.value
		await self.req.make_async_request("POST", f"/{circleId}/s/notices", {
			"uid": userId,
			"content": reason,
			"muteExpTime": actual_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
		})
		return True

	@require_auth
	async def unmute_user(self, circleId: str, userId: str, reason: str = "") -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/notices/mute/cancel", {
			"uid": userId,
			"note": reason,
		})
		return True

	@require_auth
	async def warn_user(self, circleId: str, userId: str, reason: str = "") -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/notices", {
			"uid": userId,
			"content": reason,
		})
		return True

	@require_auth
	async def switch_ban_status(self, circleId: str, userId: str, reason: str = "") -> int:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/status", {
			"note": reason
		})
		data: dict = await result.json()
		return data["objectStatus"]


	#personas--------------------------

	@require_auth
	async def get_disabled_personas(self, circleId: str, start: int = 0, limit: int = 50) -> UserPersonasList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/personas?type=1&limit={limit}&start={start}&status=0")
		return UserPersonasList(await result.json())

	@require_auth
	async def get_user_personas(self, circleId: str, userId: str, start: int = 0, limit: int = 50) -> UserPersonasList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/personas?type=0&limit={limit}&start={start}&status=0&parentId={userId}")
		return UserPersonasList(await result.json())
	
	@require_auth
	async def create_persona(self, circleId: str, nickname: str, avatar: IO | BufferedReader | AsyncBufferedReader, bio: str | None = None) -> UserPersona:
		avatar_data = await self.upload_media(avatar, MediaTarget.PersonaAvatar)
		result = await self.req.make_async_request("POST", f"/{circleId}/s/personas", {
			"nickname": nickname,
			"avatar": avatar_data.url,
			"content": bio or ""
		})
		data: dict = await result.json()
		return UserPersona(data["persona"])


	@require_auth
	async def get_persona_info(self, circleId: str, personaId: str) -> UserPersona:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/personas/{personaId}")
		data: dict = await result.json()
		return UserPersona(data["persona"])

	@require_auth
	async def delete_persona(self, circleId: str, personaId: str) -> UserPersona:
		result = await self.req.make_async_request("DELETE", f"/{circleId}/s/personas/{personaId}")
		data: dict = await result.json()
		return UserPersona(data["persona"])

	@require_auth
	async def edit_persona(self, circleId: str, personaId: str, nickname: str | None = None, avatar: IO | BufferedReader | AsyncBufferedReader | None = None, bio: str | None = None) -> UserPersona:
		if not nickname and not avatar and not bio:raise exceptions.NoDataError
		
		avatar_url = None
		if avatar:
			avatar_data = await self.upload_media(avatar, MediaTarget.PersonaAvatar)
			avatar_url = avatar_data.url
		result = await self.req.make_async_request("PUT", f"/{circleId}/s/personas/{personaId}", {
			"nickname": nickname or "",
			"avatar": avatar_url or "",
			"content": bio or ""
		})
		data: dict = await result.json()
		return UserPersona(data["persona"])
	
	async def set_persona_in_chat(self, circleId: str, chatId: str, personaId: str | None = None) -> PersonaInChat:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/members/persona", {
			"personaId": personaId
		})
		data: dict = await result.json()
		return PersonaInChat(data["member"])