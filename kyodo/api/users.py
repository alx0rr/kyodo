from kyodo.api.base import AsyncBaseClass
from kyodo.utils import require_auth, require_uid
from kyodo.objects import (
	OnlinePreview,
	OnlineUsers,
	UserProfileList,
	UserProfile,
	BlockingUsers,
	BlockingResult,
	MediaTarget,
	UserBadge
)

from kyodo.objects.args import CircleUsersType, ChatMemberTypes
from kyodo.utils.exceptions import BadArgument


from typing import IO
from _io import BufferedReader


class UserModule(AsyncBaseClass):

	@require_auth
	def get_blocked_users(self) -> BlockingUsers:
		response = self.req.make_request("GET", f"/g/s/accounts/blocking/uids")
		return BlockingUsers(response.json())
		

	@require_auth
	def get_online_preview(self, circleId: str) -> list[OnlinePreview]:
		response = self.req.make_request("GET", f"/{circleId}/s/live-activity/online-users")
		return [OnlinePreview(x) for x in (response.json()).get("userPreviewList", [])]
		

	@require_auth
	def get_online_users(self, circleId: str) -> OnlineUsers:
		response = self.req.make_request("GET", f"/{circleId}/s/live-activity")
		return OnlineUsers(response.json())

	@require_auth
	def get_circle_users(self, circleId: str, size: str = 25, type: str = CircleUsersType.Members, parentId: str | None = None, pageToken: str | None = None) -> UserProfileList:
		if type not in CircleUsersType._all: raise BadArgument(f"{type} not in CircleUsersType ({CircleUsersType._all})")
		response = self.req.make_request("GET", f"/{circleId}/s/users?type={type}&size={size}{f'&parentId={parentId}' if parentId else ''}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())
	

	@require_auth
	def get_user_profile(self, circleId: str, userId: str) -> UserProfile:
		response = self.req.make_request("GET", f"/{circleId}/s/users/{userId}")
		return UserProfile((response.json()).get("userProfile", {}))

	@require_auth
	def toggle_user_following(self, circleId: str, userId: str) -> UserProfile:
		response = self.req.make_request("POST", f"/{circleId}/s/users/{userId}/following")
		return UserProfile((response.json()).get("userProfile", {}))

	@require_auth
	def block_user(self, userId: str) -> BlockingResult:
		return BlockingResult((self.req.make_request("POST", f"/g/s/accounts/blocking", {
			"uid": userId,
			"isBlocked": True
		})).json())

	@require_auth
	def unblock_user(self, userId: str) -> BlockingResult:
		return BlockingResult((self.req.make_request("POST", f"/g/s/accounts/blocking", {
			"uid": userId,
			"isBlocked": False
		})).json())

	@require_auth
	def get_chat_users(self, chatId: str, circleId: str | None = None, type: str = ChatMemberTypes.All, size: int = 20, pageToken: str | None = None) -> UserProfileList:
		if type not in ChatMemberTypes._all: raise BadArgument(f"{type} not in ChatMemberTypes ({ChatMemberTypes._all})")
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats/{chatId}/members?type={type}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())
	

	@require_auth
	def get_user_following(self, userId: str, circleId: str | None = None, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/users?type=followers&size={size}&parentId={userId}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())
	


	@require_auth
	def get_user_followers(self, userId: str, circleId: str | None = None, size: str = 25, pageToken: str | None = None) -> UserProfileList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/users?type=following&size={size}&parentId={userId}{f'&t={pageToken}' if pageToken else ''}")
		return UserProfileList(response.json())


	@require_auth
	@require_uid
	def set_online_status(self, circleId: str | None = None, appearOnline: bool = True, content: str | None = None) -> UserProfile:
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/users/{self.userId}/status", {
			"appearOnline": appearOnline,
			"content": content or ''
		})
		return UserProfile((response.json()).get("userProfile", {}))


	@require_auth
	@require_uid
	def edit_profile(self,
			nickname: str, avatar: IO | BufferedReader | str,
			cover: IO | BufferedReader | str | None,
			fg: str = "#FFFFFF", bg: str = "#0F0F0F", circleId: str | None = None) -> UserProfile:
		
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/users/{self.userId}", {
			"nickname": nickname,
			"avatar": avatar if isinstance(avatar, str) else (self.upload_media(avatar, MediaTarget.UserAvatar)).url,
			"cover":  (cover if isinstance(cover, str) else (self.upload_media(cover, MediaTarget.UserCover)).url) if cover is not None else None,
			"theme": {
				"fg": fg,
				"bg": bg
			}
		})
		
		return UserProfile((response.json()).get("userProfile", {}))



	@require_auth
	@require_uid
	def edit_profile_description(self, bio: str, circleId: str | None = None) -> UserProfile:
		
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/users/{self.userId}", {
			"bio": bio,
			"mediaMap": {} # TODO
		})
					
		return UserProfile((response.json()).get("userProfile", {}))



	@require_auth
	def get_user_badges(self, userId: str, circleId: str | None = None) -> list[UserBadge]:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/users/{userId}/badges")
		return [UserBadge(x) for x in (response.json()).get("badgeList", [])]


	@require_auth
	def pick_topic_tag(self, topicId: str):
		self.req.make_request("POST", f"/g/s/topics/{topicId}/pick")



	@require_auth
	def unpick_topic_tag(self, topicId: str):
		self.req.make_request("POST", f"/g/s/topics/{topicId}/unpick")


	@require_auth
	def set_avatar_frame(self, avatarFrameId: str = 'none', useEverywhere: bool = False, circleId: str | None = None) -> UserProfile:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/monetization/avatar-frames/{avatarFrameId}/use", {
			"useEverywhere": useEverywhere
		})
		return UserProfile((response.json()).get("userProfile", {}))