from kyodo.api.base import BaseClass
from kyodo.utils import require_auth, require_uid
from kyodo.objects import (
	OnlinePreview,
	OnlineUsers,
	UserProfileList,
	UserProfile,
	BlockingUsers,
	BlockingResult,
	MediaTarget
)

from kyodo.objects.args import CircleUsersType, ChatMemberTypes
from kyodo.utils.exceptions import BadArgument


from aiofiles.threadpool.binary import AsyncBufferedReader
from typing import IO
from _io import BufferedReader


class UserModule(BaseClass):

	@require_auth
	async def get_blocked_users(self) -> BlockingUsers:
		response = await self.req.make_async_request("GET", f"/g/s/accounts/blocking/uids")
		return BlockingUsers(await response.json())
		

	@require_auth
	async def get_online_preview(self, circleId: str) -> list[OnlinePreview]:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/live-activity/online-users")
		return [OnlinePreview(x) for x in (await response.json()).get("userPreviewList", [])]
		

	@require_auth
	async def get_online_users(self, circleId: str) -> OnlineUsers:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/live-activity")
		return OnlineUsers(await response.json())

	@require_auth
	async def get_circle_users(self, circleId: str, size: str = 25, type: str = CircleUsersType.Members, parentId: str | None = None, pageToken: str | None = None) -> UserProfileList:
		if type not in CircleUsersType._all: raise BadArgument(f"{type} not in CircleUsersType ({CircleUsersType._all})")
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users?type={type}&size={size}{f'&parentId={parentId}' if parentId else ''}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())
	

	@require_auth
	async def get_user_profile(self, circleId: str, userId: str) -> UserProfile:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users/{userId}")
		return UserProfile((await response.json()).get("userProfile", {}))

	@require_auth
	async def toggle_user_following(self, circleId: str, userId: str) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/users/{userId}/following")
		return UserProfile((await response.json()).get("userProfile", {}))

	@require_auth
	async def block_user(self, userId: str) -> BlockingResult:
		return BlockingResult(await (await self.req.make_async_request("POST", f"/g/s/accounts/blocking", {
			"uid": userId,
			"isBlocked": True
		})).json())

	@require_auth
	async def unblock_user(self, userId: str) -> BlockingResult:
		return BlockingResult(await (await self.req.make_async_request("POST", f"/g/s/accounts/blocking", {
			"uid": userId,
			"isBlocked": False
		})).json())

	@require_auth
	async def get_chat_users(self, chatId: str, circleId: str | None = None, type: str = ChatMemberTypes.All, size: int = 20, pageToken: str | None = None) -> UserProfileList:
		if type not in ChatMemberTypes._all: raise BadArgument(f"{type} not in ChatMemberTypes ({ChatMemberTypes._all})")
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats/{chatId}/members?type={type}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())
	

	@require_auth
	async def get_user_following(self, userId: str, circleId: str | None = None, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/users?type=followers&size={size}&parentId={userId}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())
	


	@require_auth
	async def get_user_followers(self, userId: str, circleId: str | None = None, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/users?type=following&size={size}&parentId={userId}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())


	@require_auth
	@require_uid
	async def set_online_status(self, circleId: str | None = None, appearOnline: bool = True, content: str | None = None) -> UserProfile:
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/users/{self.userId}/status", {
			"appearOnline": appearOnline,
			"content": content or ''
		})
		return UserProfile((await response.json()).get("userProfile", {}))


	@require_auth
	@require_uid
	async def edit_profile(self,
			nickname: str, avatar: IO | BufferedReader | AsyncBufferedReader | str,
			cover: IO | BufferedReader | AsyncBufferedReader | str | None,
			fg: str = "#FFFFFF", bg: str = "#0F0F0F", circleId: str | None = None) -> UserProfile:
		
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/users/{self.userId}", {
			"nickname": nickname,
			"avatar": avatar if isinstance(avatar, str) else (await self.upload_media(avatar, MediaTarget.UserAvatar)).url,
			"cover":  (cover if isinstance(cover, str) else (await self.upload_media(cover, MediaTarget.UserCover)).url) if cover is not None else None,
			"theme": {
				"fg": fg,
				"bg": bg
			}
		})
		
		return UserProfile((await response.json()).get("userProfile", {}))



	@require_auth
	@require_uid
	async def edit_profile_description(self, bio: str, circleId: str | None = None) -> UserProfile:
		
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/users/{self.userId}", {
			"bio": bio,
			"mediaMap": {} # TODO
		})
					
		return UserProfile((await response.json()).get("userProfile", {}))



	@require_auth
	async def get_user_badges(self, userId: str, circleId: str | None = None) -> dict:

		#TODO ADD OBJECT

		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/users/{userId}/badges")
		return await response.json()



	@require_auth
	async def pick_topic_tag(self, topicId: str):
		await self.req.make_async_request("POST", f"/g/s/topics/{topicId}/pick")



	@require_auth
	async def unpick_topic_tag(self, topicId: str):
		await self.req.make_async_request("POST", f"/g/s/topics/{topicId}/unpick")


	@require_auth
	async def set_avatar_frame(self, avatarFrameId: str = 'none', useEverywhere: bool = False, circleId: str | None = None) -> UserProfile:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/monetization/avatar-frames/{avatarFrameId}/use", {
			"useEverywhere": useEverywhere
		})
		return UserProfile((await response.json()).get("userProfile", {}))

