from .base import BaseClass
from ..utils import require_auth, require_uid
from uuid import uuid4

from kyodo.objects import UnreadChats, ChatMessage, ChatMessageList, Chat, ChatsList
from kyodo.objects.args import ChatMessageTypes, MediaTarget

from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader

class ChatModule(BaseClass):

	@require_auth
	async def get_unread_chats(self, circleId: str | None = None) -> UnreadChats:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats/check")
		return UnreadChats(await response.json())

	@require_auth
	async def get_chat_info(self, chatId: str, circleId: str | None = None) -> Chat:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats/{chatId}")
		return Chat((await response.json()).get("chat"))

	@require_auth
	async def get_circle_chats(self, circleId: str | None = None, size: int = 25, pageToken: str | None = None) -> ChatsList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats?type=discover&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(await response.json())

	@require_auth
	async def get_joined_chats(self, circleId: str | None = None, size: int = 25,  pageToken: str | None = None) -> ChatsList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats?type=joined-active{'-global' if circleId == 'g' else ''}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(await response.json())

	@require_auth
	async def leave_chat(self, chatId: str, circleId: str | None = None) -> Chat:
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/leave")
		return Chat((await response.json()).get("chat"))
	
	@require_auth
	async def join_chat(self, chatId: str, circleId: str | None = None) -> Chat:
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/join")
		return Chat((await response.json()).get("chat"))

	@require_auth
	async def mark_as_read_chat(self, chatId: str, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/mark-as-read")
    
	@require_auth
	async def get_chat_messages(self, chatId: str, circleId: str | None = None, size: int = 25, pageToken: str | None = None) -> ChatMessageList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats/{chatId}/messages?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatMessageList(await response.json())

	@require_auth
	async def get_message_info(self, messageId: str, circleId: str | None = None) -> ChatMessage:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/messages/{messageId}")
		return ChatMessage((await response.json()).get("chatMessage"))
	
	@require_auth
	@require_uid
	async def send_chat_entity(self, chatId: str, entity: dict, message_type: int, circleId: str | None = None) -> ChatMessage:
		entity.update({
			"type": message_type,
			"refId": f"{self.userId}.{str(uuid4())}"
		})
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/messages", entity)
		return ChatMessage((await response.json()).get("chatMessage"))
	
	@require_auth
	@require_uid
	async def send_message(self, chatId: str, content: str, circleId: str | None = None, reply_message_id: str | None = None) -> ChatMessage:
		entity = {"content": content}
		if reply_message_id:entity["replyMessageId"] = reply_message_id
		return await self.send_chat_entity(chatId, entity, ChatMessageTypes.Text, circleId)

	@require_auth
	@require_uid
	async def send_sticker_message(self, chatId: str, stickerId: str, circleId: str | None = None, reply_message_id: str | None = None) -> ChatMessage:
		entity = {"stickerId": stickerId}
		if reply_message_id:entity["replyMessageId"] = reply_message_id
		return await self.send_chat_entity(chatId, entity, ChatMessageTypes.Sticker, circleId)


	@require_auth
	@require_uid
	async def send_photo(self, chatId: str, image: IO | BufferedReader | AsyncBufferedReader, circleId: str | None = None, reply_message_id: str | None = None) -> ChatMessage:
		url = (await self.upload_media(image, MediaTarget.ChatImageMessage)).url
		entity = {"content": url}
		if reply_message_id:entity["replyMessageId"] = reply_message_id
		return await self.send_chat_entity(chatId, entity, ChatMessageTypes.Photo, circleId)