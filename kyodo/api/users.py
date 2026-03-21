from .base import BaseClass
from ..utils import require_auth
from kyodo.objects import OnlinePreview, OnlineUsers, UserProfileList, UserProfile, BlockingUsers
from kyodo.objects.args import CircleUsersType, ChatMemberTypes
from kyodo.utils.exceptions import BadArgument

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
	async def get_circle_users(self, circleId: str, size: str = 25, type: str = CircleUsersType.Members) -> UserProfileList:
		if type not in CircleUsersType._all: raise BadArgument(f"{type} not in CircleUsersType ({CircleUsersType._all})")
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users?type={type}&size={size}")
		return UserProfileList(await response.json())
	

	@require_auth
	async def get_user_profile(self, circleId: str, userId: str) -> UserProfile:
		response = await self.req.make_async_request("GET", f"{circleId}/s/users/{userId}")
		return UserProfile((await response.json()).get("userProfile", {}))

	@require_auth
	async def toggle_user_following(self, circleId: str, userId: str) -> UserProfile:
		response = await self.req.make_async_request("POST", f"{circleId}/s/users/{userId}/following")
		return UserProfile((await response.json()).get("userProfile", {}))

	@require_auth
	async def block_user(self, userId: str):
		await self.req.make_async_request("POST", f"/g/s/accounts/blocking", {
			"uid": userId,
			"isBlocked": True
		})

	@require_auth
	async def unblock_user(self, userId: str):
		await self.req.make_async_request("POST", f"/g/s/accounts/blocking", {
			"uid": userId,
			"isBlocked": False
		})

	@require_auth
	async def get_chat_users(self, chatId: str, circleId: str | None = None, type: str = ChatMemberTypes.All, size: int = 20, pageToken: str | None = None) -> UserProfileList:
		if type not in ChatMemberTypes._all: raise BadArgument(f"{type} not in ChatMemberTypes ({ChatMemberTypes._all})")
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats/{chatId}/members?type={type}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())
	

	@require_auth
	async def get_user_following(self, circleId: str, userId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users?type=followers&size={size}&parentId={userId}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())
	


	@require_auth
	async def get_user_followers(self, circleId: str, userId: str, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/users?type=following&size={size}&parentId={userId}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(await response.json())