from kyodo.objects.user import UserProfile
from kyodo.objects.sticker import StickerInfo

class UnreadChats:

	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.unreadCount: int = data.get("unreadCount")
		self.invitedCount: int = data.get("invitedCount")
		self.unreadChatIds: list[str] = data.get("unreadChatIds", [])


class ChatMemberSummary:
	def __init__(self, data: dict):
		data = data or {}

		self.userId: str = data.get("uid")
		self.nickname: str = data.get("nickname")
		self.avatar: str = data.get("avatar")
		self.role: int = data.get("role")
		self.status: int = data.get("status")
		self.is_nickname_verified: bool = data.get("isNicknameVerified", False)


class ChatLastMessage:
	def __init__(self, data: dict):
		data = data or {}

		self.messageId: str = data.get("id")
		self.userId: str = data.get("user", {}).get("uid")

		self.content: str = data.get("content")
		self.type: int = data.get("type")
		self.status: int = data.get("status")

		self.author: UserProfile = UserProfile(data.get("user", {}))



class ChatMember:
	def __init__(self, data: dict):
		data = data or {}

		self.userId: str = data.get("uid")
		self.status: int = data.get("status")
		self.position_type: int = data.get("positionType")
		self.last_read_time: str = data.get("lastReadTime")
		self.do_not_disturb: bool = data.get("doNotDisturb", False)

class Chat:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.chatId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")

		self.name: str = data.get("name")
		self.icon: str = data.get("icon")

		self.type: int = data.get("type")
		self.status: int = data.get("status")

		self.memberCount: int = data.get("memberCount")
		self.memberLimit: int = data.get("memberLimit")

		
		self.memberSummary: list[ChatMemberSummary] = [
			ChatMemberSummary(x) for x in data.get("memberSummary", [])
		]

		
		self.lastMessage: ChatLastMessage = ChatLastMessage(data.get("lastMessage"))

		
		self.member: ChatMember = ChatMember(data.get("member"))

		self.lastActiveTime: str = data.get("lastActiveTime")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")

		self.background = data.get("background")
		self.extensions: dict = data.get("extensions", {})

		self.coHostUids: list = data.get("coHostUids", [])

		self.isReadOnly: bool = data.get("isReadOnly", False)
		self.content = data.get("content")



class ChatsList:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.pagination: dict = data.get("pagination", {})

		self.chats: list[Chat] = [Chat(x) for x in data.get("chatList", [])]


class ChatReplyMessage:
	def __init__(self, data: dict):
		data = data or {}

		self.data = data
		self.messageId: str = data.get("id")
		self.userId: str = data.get("user", {}).get("uid")

		self.content: str = data.get("content")
		self.type: int = data.get("type")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")

		self.author: UserProfile = UserProfile(data.get("user", {}))

		self.sticker: StickerInfo = StickerInfo(data.get("sticker", {}))



class ChatMessage:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.chatId: str = data.get("chatId")
		self.circleId: str = data.get("circleId")

		self.messageId: str = data.get("id")
		self.refId: str = data.get("refId")

		self.userId: str = data.get("uid")
		self.content: str = data.get("content")

		self.type: int = data.get("type")
		self.status: int = data.get("status")

		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")

		self.author: UserProfile = UserProfile(data.get("user", {}))

		self.replyMessageId: str = data.get("replyMessageId")
		self.replyMessage: ChatReplyMessage = ChatReplyMessage(data.get("replyMessage", {}))

		self.mentionedUids: list = data.get("mentionUids", [])

		self.sticker: StickerInfo = StickerInfo(data.get("sticker", {}))


class ChatMessageList:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data
		self.pagination: dict = data.get("pagination", {})

		self.messages: list[ChatMessage] = [ChatMessage(x) for x in data.get("messageList", [])]



class DeleteChatMessage:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data
		self.chatId: str = data.get("chatId")
		self.messageId: str = data.get("messageId")
		self.circleId: str = data.get("circleId")