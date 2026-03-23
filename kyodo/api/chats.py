from kyodo.api.base import BaseClass
from kyodo.utils import require_auth, require_uid
from kyodo.objects import UnreadChats, ChatMessage, ChatMessageList, Chat, ChatsList, ChatMember, StickerInfo, StickerList, StickerPackList
from kyodo.objects.args import ChatMessageTypes, MediaTarget, ChatType


from uuid import uuid4
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
	async def get_direct_chat(self, userId: str, circleId: str | None = None) -> Chat:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats/direct?uid={userId}")
		return Chat((await response.json()).get("chat"))


	@require_auth
	async def get_invited_chats(self, circleId: str | None = None, size: int = 25,  pageToken: str | None = None) -> ChatsList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats?type=invited&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(await response.json())


	@require_auth
	async def get_user_hosted_chats(self, userId: str, circleId: str | None = None, size: int = 25,  pageToken: str | None = None) -> ChatsList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/chats?type=user-hosted&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(await response.json())



	@require_auth
	async def start_direct_chat(self, userId: str, circleId: str | None = None, message: str | None = None) -> tuple[Chat, ChatMessageList]:
		payload = {
			"type": ChatType.PRIVATE,
			"inviteeUids": [userId,]
		}
		if message:payload["initialMessage"] = message
		data = await (await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats", payload)).json()
		return (Chat(data.get("chat", {})), ChatMessageList({"messageList": data.get("messageList", {})}))


	@require_auth
	async def start_group_chat(self, userIds: list, circleId: str | None = None) -> tuple[Chat, ChatMessageList]:
		payload = {
			"type": ChatType.GROUP,
			"inviteeUids": userIds
		}
		data = await (await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats", payload)).json()
		return (Chat(data.get("chat", {})), ChatMessageList({"messageList": data.get("messageList", {})}))



	@require_auth
	async def start_public_chat(self, image: IO | BufferedReader | AsyncBufferedReader, title: str, content: str | None = None, circleId: str | None = None) -> tuple[Chat, ChatMessageList]:
		url = (await self.upload_media(image, MediaTarget.ChatIcon)).url
		data = await (await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats", {
			"type": ChatType.PUBLIC,
			"name": title,
			"content": content or '',
			"icon": url
		})).json()
		return (Chat(data.get("chat", {})), ChatMessageList({"messageList": data.get("messageList", {})}))




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


	@require_auth
	async def delete_message(self, messageId: str, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/messages/{messageId}/delete")


	
	@require_auth
	async def save_sticker(self, packId: str, image: IO | BufferedReader | AsyncBufferedReader, circleId: str | None = None) -> StickerInfo:
		url = (await self.upload_media(image, MediaTarget.StickerImage)).url
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/monetization/stickers/packs/{packId}/save-sticker", {"mediaUrl": url})
		return StickerInfo((await response.json()).get("sticker", {}))
	
	@require_auth
	async def get_my_sticker_packs(self, circleId: str | None = None, size: int = 20, pageToken: str | None = None) -> StickerPackList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/monetization/stickers/packs?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return StickerPackList(await response.json())

	@require_auth
	async def get_stickers(self, packId: str, circleId: str | None = None, size: int = 50, pageToken: str | None = None) -> StickerList:
		response = await self.req.make_async_request("GET", f"/{circleId or 'g'}/s/monetization/stickers?packId={packId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return StickerList(await response.json())


	@require_auth
	async def mute_chat(self, chatId: str, circleId: str | None = None, isMuted: bool = True) -> ChatMember:
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/mute", {
			"isMuted": isMuted
		})
		return ChatMember((await response.json()).get("chatMember", {}))

	@require_auth
	async def set_chat_read_only(self, chatId: str, circleId: str | None = None, isReadOnly: bool = True):
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/read-only", {
			"isReadOnly": isReadOnly
		})
		return Chat((await response.json()).get("chat", {}))


	@require_auth
	async def equip_chat_persona(self, chatId: str, personaId: str, circleId: str | None = None) -> ChatMember:
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/select-persona", {
			"personaId": personaId
		})
		return ChatMember((await response.json()).get("chatMember", {}))




	@require_auth
	async def set_chat_wallpaper(self, image: IO | BufferedReader | AsyncBufferedReader, chatId: str, circleId: str | None = None) -> Chat:
		url = (await self.upload_media(image, MediaTarget.ChatBackground)).url
		response = await (await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/wallpaper", {"wallpaper": url}))
		return Chat((await response.json()).get("chat"))


	@require_auth
	async def edit_chat(self, chatId: str, name: str | None = None, content: str | None = None, icon: IO | BufferedReader | AsyncBufferedReader | None = None, circleId: str | None = None) -> Chat:
		payload = {}

		if icon is not None:
			payload["icon"] = (await self.upload_media(icon, MediaTarget.ChatBackground)).url
		if name is not None:
			payload["name"] = name
		if content is not None:
			payload["content"] = content
			payload["mediaMap"] = {}#TODO

		if payload:
			response = await (await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}", payload))
			return Chat((await response.json()).get("chat"))
		return Chat({})
	

	@require_auth
	async def add_chat_cohost(self, chatId: str, userIds: str | list, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/co-hosts", {
			"uids": userIds if isinstance(userIds, list) else [userIds,]
		})

	@require_auth
	async def remove_chat_cohost(self, chatId: str, userId: str, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/remove-co-host")

	@require_auth
	async def transfer_chat_host(self, chatId: str, userId: str, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/transfer-host")

	@require_auth
	async def kick(self, chatId: str, userId: str, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/kick")

	@require_auth
	async def unkick(self, chatId: str, userId: str, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/unkick")


	@require_auth
	async def disable_chat(self, chatId: str, circleId: str | None = None, note: str | None = None) -> Chat:
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/disable", {"note": note or ''})
		return Chat((await response.json()).get("chat"))


	@require_auth
	async def enable_chat(self, chatId: str, circleId: str | None = None, note: str | None = None) -> Chat:
		response = await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/enable", {"note": note or ''})
		return Chat((await response.json()).get("chat"))


	@require_auth
	async def invite_to_chat(self, chatId: str, userIds: str | list, circleId: str | None = None):
		await self.req.make_async_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/invite", {
			"inviteeUids": userIds if isinstance(userIds, list) else [userIds,]
		})
