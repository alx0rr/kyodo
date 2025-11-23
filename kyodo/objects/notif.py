from . import BaseProfile, Circle

class NoticesList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.notices: list[Notice] = [Notice(notice) for notice in data.get("notices", [])]
		self.hasMore: bool = data.get("hasMore")


class NotificationsList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.notifications: list[Notification] = [Notification(notification) for notification in data.get("notifications", [])]
		self.hasMore: bool = data.get("hasMore")



class Notice:
	def __init__(self, data: dict):
		self.data: dict = data
		self.noticeId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.operatorId: str = data.get("operatorId")
		self.title: str = data.get("title")
		self.level: int = data.get("level")
		self.label: str = data.get("label")
		self.status: int = data.get("status")
		self.content: int = data.get("content")
		self.quickActions: list[dict] = data.get("quickActions")
		self.createdTime: str = data.get("createdTime")
		self.circle: Circle = Circle(data.get("circle", {}))


class Notification:
	def __init__(self, data: dict):
		self.data: dict = data
		self.notificationId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")
		self.opId: str = data.get("opId")
		self.type: int = data.get("type")
		self.objectId: str = data.get("objectId")
		self.objectType: str = data.get("objectType")
		self.objectText: str | None = data.get("objectText")

		paths: dict = data.get("paths")

		self.apiPath: str = paths.get("api")
		self.appPath: str = paths.get("app")
		self.content: str = data.get("content")
		self.isRead: bool = data.get("isRead")
		self.createdTime: str = data.get("createdTime")
		self.op: BaseProfile = BaseProfile(data.get("op", {}))