from kyodo.api.base import SyncBaseClass
from kyodo.utils import require_auth, require_uid
from kyodo.objects import(
	UnreadChats,
	ChatMessage,
	ChatMessageList,
	Chat,
	ChatsList,
	ChatMember,
	StickerInfo,
	StickerList, 
	StickerPackList
)
from kyodo.objects.args import ChatMessageTypes, MediaTarget, ChatType


from uuid import uuid4
from typing import IO
from _io import BufferedReader

class ChatModule(SyncBaseClass):

	@require_auth
	def get_unread_chats(self, circleId: str | None = None) -> UnreadChats:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats/check")
		return UnreadChats(response.json())

	@require_auth
	def get_chat_info(self, chatId: str, circleId: str | None = None) -> Chat:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats/{chatId}")
		return Chat((response.json()).get("chat"))

	@require_auth
	def get_circle_chats(self, circleId: str | None = None, size: int = 25, pageToken: str | None = None) -> ChatsList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats?type=discover&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(response.json())

	@require_auth
	def get_joined_chats(self, circleId: str | None = None, size: int = 25,  pageToken: str | None = None) -> ChatsList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats?type=joined-active{'-global' if circleId == 'g' else ''}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(response.json())


	@require_auth
	def get_direct_chat(self, userId: str, circleId: str | None = None) -> Chat:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats/direct?uid={userId}")
		return Chat((response.json()).get("chat"))


	@require_auth
	def get_invited_chats(self, circleId: str | None = None, size: int = 25,  pageToken: str | None = None) -> ChatsList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats?type=invited&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(response.json())


	@require_auth
	def get_user_hosted_chats(self, userId: str, circleId: str | None = None, size: int = 25,  pageToken: str | None = None) -> ChatsList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats?type=user-hosted&parentId={userId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatsList(response.json())



	@require_auth
	def start_direct_chat(self, userId: str, circleId: str | None = None, message: str | None = None) -> tuple[Chat, ChatMessageList]:
		payload = {
			"type": ChatType.PRIVATE,
			"inviteeUids": [userId,]
		}
		if message:payload["initialMessage"] = message
		data = (self.req.make_request("POST", f"/{circleId or 'g'}/s/chats", payload)).json()
		return (Chat(data.get("chat", {})), ChatMessageList({"messageList": data.get("messageList", {})}))


	@require_auth
	def start_group_chat(self, userIds: list, circleId: str | None = None) -> tuple[Chat, ChatMessageList]:
		payload = {
			"type": ChatType.GROUP,
			"inviteeUids": userIds
		}
		data = (self.req.make_request("POST", f"/{circleId or 'g'}/s/chats", payload)).json()
		return (Chat(data.get("chat", {})), ChatMessageList({"messageList": data.get("messageList", {})}))



	@require_auth
	def start_public_chat(self, image: IO | BufferedReader, title: str, content: str | None = None, circleId: str | None = None) -> tuple[Chat, ChatMessageList]:
		url = (self.upload_media(image, MediaTarget.ChatIcon)).url
		data = (self.req.make_request("POST", f"/{circleId or 'g'}/s/chats", {
			"type": ChatType.PUBLIC,
			"name": title,
			"content": content or '',
			"icon": url
		})).json()
		return (Chat(data.get("chat", {})), ChatMessageList({"messageList": data.get("messageList", {})}))




	@require_auth
	def leave_chat(self, chatId: str, circleId: str | None = None) -> Chat:
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/leave")
		return Chat((response.json()).get("chat"))
	
	@require_auth
	def join_chat(self, chatId: str, circleId: str | None = None) -> Chat:
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/join")
		return Chat((response.json()).get("chat"))

	@require_auth
	def mark_as_read_chat(self, chatId: str, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/mark-as-read")
    
	@require_auth
	def get_chat_messages(self, chatId: str, circleId: str | None = None, size: int = 25, pageToken: str | None = None) -> ChatMessageList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/chats/{chatId}/messages?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return ChatMessageList(response.json())

	@require_auth
	def get_message_info(self, messageId: str, circleId: str | None = None) -> ChatMessage:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/messages/{messageId}")
		return ChatMessage((response.json()).get("chatMessage"))
	
	@require_auth
	@require_uid
	def send_chat_entity(self, chatId: str, entity: dict, message_type: int, circleId: str | None = None) -> ChatMessage:
		entity.update({
			"type": message_type,
			"refId": f"{self.userId}.{str(uuid4())}"
		})
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/messages", entity)
		return ChatMessage((response.json()).get("chatMessage"))
	
	@require_auth
	@require_uid
	def send_message(self, chatId: str, content: str, circleId: str | None = None, reply_message_id: str | None = None) -> ChatMessage:
		entity = {"content": content}
		if reply_message_id:entity["replyMessageId"] = reply_message_id
		return self.send_chat_entity(chatId, entity, ChatMessageTypes.Text, circleId)

	@require_auth
	@require_uid
	def send_sticker_message(self, chatId: str, stickerId: str, circleId: str | None = None, reply_message_id: str | None = None) -> ChatMessage:
		entity = {"stickerId": stickerId}
		if reply_message_id:entity["replyMessageId"] = reply_message_id
		return self.send_chat_entity(chatId, entity, ChatMessageTypes.Sticker, circleId)


	@require_auth
	@require_uid
	def send_photo(self, chatId: str, image: IO | BufferedReader, circleId: str | None = None, reply_message_id: str | None = None) -> ChatMessage:
		url = (self.upload_media(image, MediaTarget.ChatImageMessage)).url
		entity = {"content": url}
		if reply_message_id:entity["replyMessageId"] = reply_message_id
		return self.send_chat_entity(chatId, entity, ChatMessageTypes.Photo, circleId)


	@require_auth
	def delete_message(self, messageId: str, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/messages/{messageId}/delete")


	
	@require_auth
	def save_sticker(self, packId: str, image: IO | BufferedReader, circleId: str | None = None) -> StickerInfo:
		url = (self.upload_media(image, MediaTarget.StickerImage)).url
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/monetization/stickers/packs/{packId}/save-sticker", {"mediaUrl": url})
		return StickerInfo((response.json()).get("sticker", {}))
	
	@require_auth
	def get_my_sticker_packs(self, circleId: str | None = None, size: int = 20, pageToken: str | None = None) -> StickerPackList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/monetization/stickers/packs?size={size}{f'&t={pageToken}' if pageToken else ''}")
		return StickerPackList(response.json())

	@require_auth
	def get_stickers(self, packId: str, circleId: str | None = None, size: int = 50, pageToken: str | None = None) -> StickerList:
		response = self.req.make_request("GET", f"/{circleId or 'g'}/s/monetization/stickers?packId={packId}&size={size}{f'&t={pageToken}' if pageToken else ''}")
		return StickerList(response.json())


	@require_auth
	def mute_chat(self, chatId: str, circleId: str | None = None, isMuted: bool = True) -> ChatMember:
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/mute", {
			"isMuted": isMuted
		})
		return ChatMember((response.json()).get("chatMember", {}))

	@require_auth
	def set_chat_read_only(self, chatId: str, circleId: str | None = None, isReadOnly: bool = True):
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/read-only", {
			"isReadOnly": isReadOnly
		})
		return Chat((response.json()).get("chat", {}))


	@require_auth
	def equip_chat_persona(self, chatId: str, personaId: str, circleId: str | None = None) -> ChatMember:
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/select-persona", {
			"personaId": personaId
		})
		return ChatMember((response.json()).get("chatMember", {}))




	@require_auth
	def set_chat_wallpaper(self, image: IO | BufferedReader, chatId: str, circleId: str | None = None) -> Chat:
		url = (self.upload_media(image, MediaTarget.ChatBackground)).url
		response = (self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/wallpaper", {"wallpaper": url}))
		return Chat((response.json()).get("chat"))


	@require_auth
	def edit_chat(self, chatId: str, name: str | None = None, content: str | None = None, icon: IO | BufferedReader | None = None, circleId: str | None = None) -> Chat:
		payload = {}

		if icon is not None:
			payload["icon"] = (self.upload_media(icon, MediaTarget.ChatBackground)).url
		if name is not None:
			payload["name"] = name
		if content is not None:
			payload["content"] = content
			payload["mediaMap"] = {}#TODO

		if payload:
			response = (self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}", payload))
			return Chat((response.json()).get("chat"))
		return Chat({})
	

	@require_auth
	def add_chat_cohost(self, chatId: str, userIds: str | list, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/co-hosts", {
			"uids": userIds if isinstance(userIds, list) else [userIds,]
		})

	@require_auth
	def remove_chat_cohost(self, chatId: str, userId: str, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/remove-co-host")

	@require_auth
	def transfer_chat_host(self, chatId: str, userId: str, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/transfer-host")

	@require_auth
	def kick(self, chatId: str, userId: str, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/kick")

	@require_auth
	def unkick(self, chatId: str, userId: str, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/{userId}/unkick")


	@require_auth
	def disable_chat(self, chatId: str, circleId: str | None = None, note: str | None = None) -> Chat:
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/disable", {"note": note or ''})
		return Chat((response.json()).get("chat"))


	@require_auth
	def enable_chat(self, chatId: str, circleId: str | None = None, note: str | None = None) -> Chat:
		response = self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/enable", {"note": note or ''})
		return Chat((response.json()).get("chat"))


	@require_auth
	def invite_to_chat(self, chatId: str, userIds: str | list, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/chats/{chatId}/members/invite", {
			"inviteeUids": userIds if isinstance(userIds, list) else [userIds,]
		})


	@require_auth
	def set_chat_bubble(self, chatId: str, bubbleId: str = 'none', useAsDefault: bool = False, circleId: str | None = None):
		self.req.make_request("POST", f"/{circleId or 'g'}/s/monetization/chat-bubbles/{bubbleId}/use", {
			"chatId": chatId,
			"useAsDefault": useAsDefault
		})
