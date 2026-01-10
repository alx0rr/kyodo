from .base import BaseClass
from ..objects import (
	MediaTarget, ChatData, ChatMessage, ChatMessageTypes, ChatList, PersonaInChat,
	MessagesList, ChatType
)
from ..utils import require_auth, exceptions
from ..utils.generators import random_ascii_string

from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader


class ChatsModule(BaseClass):

	@require_auth
	async def get_my_chats(self, circleId: str | None = None, only_circle_chats: bool = False, start: int = 0, limit: int = 20) -> ChatList:
		chat_type = 1 if only_circle_chats else 0
		result = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats?type={chat_type}&start={start}&limit={limit}")
		return ChatList(await result.json())


	@require_auth
	async def get_circle_disabled_chats(self, circleId: str, start: int = 0, limit: int = 15) -> ChatList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/feed?type=latest&start={start}&limit={limit}&status=1")
		return ChatList(await result.json())

	@require_auth
	async def get_circle_chats(self, circleId: str, start: int = 0, limit: int = 15) -> ChatList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/feed?type=hottest&start={start}&limit={limit}&status=0")
		return ChatList(await result.json())


	@require_auth
	async def has_unread_chats(self) -> bool:
		result = await self.req.make_async_request("GET", f"/g/s/chats/unread")
		data: dict = await result.json()
		return data["hasUnread"]

	@require_auth
	async def join_chat(self, circleId: str, chatId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/join")
		return True

	@require_auth
	async def leave_chat(self, circleId: str, chatId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/leave")
		return True

	@require_auth
	async def mark_as_read_chat(self, circleId: str, chatId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/read")
		return True

	@require_auth
	async def edit_chat(self, circleId: str, chatId: str, name: str | None = None, content: str | None = None, icon: IO | BufferedReader | AsyncBufferedReader | None = None, background: IO | BufferedReader | AsyncBufferedReader | None = None) -> bool:
		data = {}
		if name:
			data["name"] = name
		if content:
			data["content"] = content
		if background:
			background_data = await self.upload_media(background, MediaTarget.ChatBackground)
			data["background"] = background_data.url
		if icon:
			icon_data = await self.upload_media(icon, MediaTarget.ChatIcon)
			data["icon"] = icon_data.url
		if not data:raise exceptions.NoDataError

		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}", data)
		return True

	@require_auth
	async def create_public_chat(self, circleId: str, name: str, icon: IO | BufferedReader | AsyncBufferedReader, invitedIds: list = []) -> ChatData:
		icon_data = await self.upload_media(icon, MediaTarget.ChatIcon)

		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats", {
			"name": name,
			"type": ChatType.PUBLIC,
			"icon": icon_data.url,
			"invitedIds": invitedIds
		})

		return ChatData(await result.json())

	@require_auth
	async def create_group_chat(self, circleId: str, invitedIds: list[str]) -> ChatData:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats", {
			"type": ChatType.GROUP,
			"invitedIds": invitedIds
		})

		return ChatData(await result.json())

	@require_auth
	async def start_direct_chat(self, circleId: str, userId: str) -> ChatData:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats", {
			"type": ChatType.PRIVATE,
			"invitedIds": [userId]
		})
		return ChatData((await result.json()).get("chat", {}))


	@require_auth
	async def disable_enable_chat(self, circleId: str, chatId: str, reason: str) -> bool:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/status",{
			"note": reason
		})
		data: dict = await result.json()
		return bool(data["objectStatus"])


	@require_auth
	async def delete_chat(self, circleId: str, chatId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/leave", {
		"confirmAsHost" : True
		})
		return True

	@require_auth
	async def chat_not_disturb(self, circleId: str, chatId) -> PersonaInChat:
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/members/do-not-disturb")
		return PersonaInChat(await result.json())

	@require_auth
	async def delete_message(self, circleId: str, chatId: str, messageId: str) -> bool:
		await self.req.make_async_request("DELETE", f"/{circleId}/s/chats/{chatId}/messages/{messageId}")
		return True

	@require_auth
	async def transfer_chat_host(self, circleId: str, chatId: str, userId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/members/host-transfer", {"uid": userId})
		return True

	@require_auth
	async def add_chat_cohost(self, circleId: str, chatId: str, userId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/members/cohosts ", {"uid": userId})
		return True


	@require_auth
	async def delete_chat_cohost(self, circleId: str, chatId: str, userId: str) -> bool:
		await self.req.make_async_request("DELETE", f"/{circleId}/s/chats/{chatId}/members/cohosts/{userId} ")
		return True

	@require_auth
	async def chat_read_only(self, circleId: str, chatId: str) -> None:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/read-only")
		return None


	@require_auth
	async def kick(self, circleId: str, chatId: str, userId: str) -> bool:
		await self.req.make_async_request("DELETE", f"/{circleId}/s/chats/{chatId}/members/{userId}")
		return True
	

	@require_auth
	async def unkick(self, circleId: str, chatId: str, userId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/members/{userId}/unkick")
		return True

	@require_auth
	async def get_chat_info(self, circleId: str, chatId: str) -> ChatData:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/{chatId}")
		data = await result.json()
		return ChatData(data.get("chat", {}))

	@require_auth
	async def get_chat_messages(self, circleId: str, chatId: str, start: int = 0, limit: int = 15) -> MessagesList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/chats/{chatId}/messages?start={start}&limit={limit}")
		return MessagesList(await result.json())

	@require_auth
	async def send_message(self, circleId: str, chatId: str, message: str, replyMessageId: str | None = None) -> ChatMessage:
		return await self.send_entity_to_chat(circleId, chatId, {"content": message}, replyMessageId, ChatMessageTypes.Text)

	@require_auth
	async def send_sticker_message(self, circleId: str, chatId: str, stickerId: str) -> ChatMessage:
		return await self.send_entity_to_chat(circleId, chatId, {"content":"-"}, type=ChatMessageTypes.Sticker, stickerId=stickerId)

	@require_auth
	async def send_photo(self, circleId: str, chatId: str, image: IO | BufferedReader | AsyncBufferedReader, replyMessageId: str | None = None) -> ChatMessage:
		icon_data = await self.upload_media(image, MediaTarget.ChatImageMessage)
		return await self.send_entity_to_chat(circleId, chatId, {"content": icon_data.url}, replyMessageId, ChatMessageTypes.Photo)

	@require_auth
	async def send_video(self, circleId: str, chatId: str, video: IO | BufferedReader | AsyncBufferedReader, replyMessageId: str | None = None) -> ChatMessage:
		icon_data = await self.upload_media(video, MediaTarget.ChatVideoMessage)
		return await self.send_entity_to_chat(circleId, chatId, {"content": icon_data.url}, replyMessageId, ChatMessageTypes.Video)

	@require_auth
	async def join_voice_chat(self, circleId: str, chatId: str) -> dict:
		#TODO
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/live-activity/voice?joinType=speak")
		return await result.json()

	@require_auth
	async def leave_voice_chat(self, circleId: str, chatId: str) -> dict:
		#TODO
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/live-activity/voice?joinType=listen")
		return await result.json()

	@require_auth
	async def voice_chat_join_permission(self, circleId: str, chatId: str, is_invite_only: bool = False) -> bool:
		#TODO
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/live-activity/privacy", {"privacy": 2 if is_invite_only else 0})
		return True

	@require_auth
	async def send_entity_to_chat(self, circleId: str, chatId: str, entity: dict, replyMessageId: str | None = None, type: int | None = 0, stickerId: str | None = None) -> ChatMessage:
		
		if "config" not in entity:
			entity["config"] = {"refId": random_ascii_string(), "type": type}
			if stickerId:entity["config"]["stickerId"] = stickerId
		if replyMessageId:
			entity["config"]["replyMessageId"] = replyMessageId
		
		result = await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/messages", entity)
		return ChatMessage(await result.json())


	@require_auth
	async def read_chat(self, circleId: str, chatId: str) -> bool:
		await self.req.make_async_request("POST", f"/{circleId}/s/chats/{chatId}/read")
		return True
