


class KyodoEventBanner:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data
		self.mediaId: str = data.get("mediaId")
		self.mediaUrl: str = data.get("mediaUrl")

class KyodoEvent:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data
		self.id: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.name: str = data.get("name")
		self.status: int = data.get("status")
		self.topic: str = data.get("topic")
		self.language: str = data.get("language")
		self.requestTime: str = data.get("requestTime")
		self.startTime: str = data.get("startTime")
		self.endTime: str = data.get("id")

		self.banner: KyodoEventBanner = KyodoEventBanner(data.get("bannerObject", {}))

		extensions = data.get("extensions", {})

		self.hadBanner: bool = extensions.get("hadBanner")
		self.statusMsg: str = extensions.get("statusMsg")
		self.bannerTime: int = extensions.get("bannerTime")
		self.bannerModuleId: str = extensions.get("bannerModuleId")


class KyodoEventList:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data
		self.pagination: dict = data.get("pagination")
		self.events: list[KyodoEvent] = [KyodoEvent(event) for event in self.data.get("eventList", [])]