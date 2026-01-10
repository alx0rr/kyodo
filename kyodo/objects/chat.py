from . import BaseProfile, ChatMessage


class ChatList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.chats: list[ChatData] = [ChatData(chat) for chat in data.get("chats", [])]
		self.hasMore: bool = data.get("hasMore")

class PersonaInChat:
	def __init__(self, data: dict):
		self.data: dict = data
		self.id: str = data.get("id")
		self.status: int = data.get("status")
		self.isMentioned: bool = data.get("isMentioned")
		self.doNotDisturb: bool = data.get("doNotDisturb")
		self.personaId: str = data.get("personaId")
		self.persona: str = data.get("persona")
		self.lastActiveTime: str = data.get("lastActiveTime")

class ChatData:
	def __init__(self, data: dict):
		
		self.data: dict = data
		self.hostId: str = data.get("hostId")
		self.hostId: list[str] = data.get("coHostIds", [])
		self.background: str = data.get("background")
		self.content: str = data.get("content")
		self.host: BaseProfile | None = BaseProfile(data.get("host")) if data.get("host") else None 
		self.activityUsers: list[str] = data.get("activityUsers")
		self.chatId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.condition: int = data.get("condition")
		self.icon: str = data.get("icon")
		self.name: str = data.get("name")
		self.type: int = data.get("type")
		self.status: int = data.get("status")

		self.activityType: int = data.get("activityType")
		self.activityPrivacy: int = data.get("activityPrivacy")
		self.specialBadge: int = data.get("specialBadge")
		self.memberCount: int = data.get("memberCount")
		self.memberLimit: int = data.get("memberLimit")
		self.readOnly: bool = data.get("readOnly")
		self.memberSummary: list[BaseProfile] = [BaseProfile(user) for user in data.get("memberSummary", [])]
		self.member: PersonaInChat = PersonaInChat(data.get("member")) #persona in chat
		self.lastMessage: ChatMessage = ChatMessage(data.get("lastMessage"))
		self.lastActiveTime: str = data.get("lastActiveTime")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")
