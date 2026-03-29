from kyodo.objects.circles import Circle
from kyodo.objects.user import UserProfile

from dataclasses import dataclass, asdict
import jwt

@dataclass
class JWTPayload:
	auth_token: str | None = None
	id: str | None = None
	email: str | None = None
	role: int | None = None
	premium_type: int | None = None
	language: str | None = None
	is_staff_member: bool | None = None
	iat: int | None = None
	exp: int | None = None

	@classmethod
	def from_token(cls, token: str):
		data = jwt.decode(token, options={"verify_signature": False})
		return cls(**data)

	@property
	def data(self) -> dict:
		return asdict(self)

	def __getitem__(self, key):
		return self.data.get(key)


class LanguageInfo:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.code: str = data.get("id")
		self.title: str = data.get("title")

class AvailableLanguages:

	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.language: str = data.get("language")
		self.contentRegion: str = data.get("contentRegion")
		self.languageList: list[LanguageInfo] = [LanguageInfo(x) for x in data.get("languageList", [])]







class ShareLinkObject:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

class ShareLink:
	def __init__(self, data: dict):
		self.data: dict = data
		share_link: dict = data.get("shareLink", {})

		self.objectPreview: ShareLinkObject = ShareLinkObject(data.get("objectPreview", {}))
		self.circle : Circle = Circle(data.get("circle", {}))

		self.id: str = share_link.get("id")
		self.circleId: str = share_link.get("circleId")
		self.objectId: str = share_link.get("objectId")
		self.objectType: int = share_link.get("objectType")



class Topic:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.id: str = data.get("id")
		self.name: str = data.get("name")
		self.slug: str = data.get("slug")

		self.score: int = data.get("score", 0)

		self.fg_color: str = data.get("fgColor")
		self.bg_color: str = data.get("bgColor")
		self.alpha_color: str = data.get("alphaColor")

		self.is_picked: bool = data.get("isPicked", False)


class AuditLog:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.id: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.objectId: str = data.get("objectId")
		self.objectType: int = data.get("objectType")
		self.operatorUid: str = data.get("operatorUid")

		self.operation: int = data.get("operation")
		self.content: str = data.get("content")
		self.level: int = data.get("level")
		self.label: str = data.get("label")

		self.created_time: str = data.get("createdTime")

		self.operator: UserProfile = UserProfile(data.get("operator", {}))

class AuditLogList:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data
		
		self.auditLogs: AuditLog = [AuditLog(x) for x in data.get("auditLogList", [])]

		self.pagination: dict = data.get("pagination", {})







class Notice:
    def __init__(self, data: dict):
        data = data or {}
        self.id: str = data.get("id")
        self.circleId: str = data.get("circleId")
        self.userId: str = data.get("uid")
        self.opUserId: str = data.get("opUid")
        self.title: str = data.get("title")
        self.content: str = data.get("content")
        self.status: int = data.get("status")
        self.level: int = data.get("level")
        self.label: str = data.get("label")
        self.created_time: str = data.get("createdTime")
        self.modified_time: str = data.get("modifiedTime")
        self.operator: UserProfile = UserProfile(data.get("operator", {}))
        self.quick_actions: list[dict] = data.get("quickActionList", [])



class NoticeList:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data
		
		self.noticeList: Notice = [Notice(x) for x in data.get("noticeList", [])]

		self.pagination: dict = data.get("pagination", {})



class Notification:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data
		
		self.id: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")
		self.type: int = data.get("type")
		self.objectId: str = data.get("objectId")
		self.objectType: int = data.get("objectType")
		self.content: str = data.get("content")
		self.is_read: int = data.get("isRead")
		self.created_time: str = data.get("createdTime")
		self.operator: UserProfile = UserProfile(data.get("operator", {}))





class NotificationList:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data
		
		self.notificationList: Notification = [Notification(x) for x in data.get("notificationList", [])]

		self.pagination: dict = data.get("pagination", {})



class Pagination:
	def __init__(self, data: dict):
		data = data or {}
		self.data = data

		self.fwd: str | int = data.get("fwd")
