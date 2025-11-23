from . import BaseProfile


class ChatReplyMessage:
	def __init__(self, data: dict = {}):
		self.data: dict = data
		self.messageId: str = data.get("id")
		self.userId: str = data.get("uid")
		self.content: str = data.get("content")
		self.author: BaseProfile = BaseProfile(data.get('author', {}))
		self.type: int = data.get("type")
		self.status: int = data.get("status")

class ChatMessage:
	def __init__(self, data: dict = {}):
		self.data: dict = data
		message: dict = self.data.get("messageItem", self.data.get("message", {}))
		self.chatId: str = message.get("chatId")
		self.circleId: str = message.get("circleId")
		self.messageId: str = message.get("id")
		self.refId: str = message.get("refId")
		self.userId: str = message.get("uid")
		self.content: str = message.get("content")
		self.type: int = message.get("type")
		self.status: int = message.get("status")
		self.stickerId: str = message.get("stickerId")
		self.createdTime: str = message.get("createdTime")

		self.author: BaseProfile = BaseProfile(message.get('author', {}))
		self.replyMessage: ChatMessage = ChatReplyMessage(message.get("replyMessage", {}))

		self.mentionedUids: list = self.data.get("mentionedUids")



class MessagesList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.messages: list[ChatMessage] = [ChatMessage(message) for message in data.get("messages", [])]
		self.hasMore: bool = data.get("hasMore")

