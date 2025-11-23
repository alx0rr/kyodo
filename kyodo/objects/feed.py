from . import Circle, PostInfo, KyodoObjectTypes, CircleInfo

class Feed:
	def __init__(self, data: dict):
		self.data: dict = data
		self.circleId: str = data.get("circleId")
		self.objectId: str = data.get("objectId")
		self.objectType: int = data.get("objectType")	
		self.content: str = data.get("content")
		self.createdTime: str = data.get("createdTime")
		self.circleId: str = data.get("circleId")
		self.object: PostInfo | CircleInfo | None

		match self.objectType:
			case KyodoObjectTypes.Post:self.object = PostInfo(data.get("object"))
			case KyodoObjectTypes.Circle:self.object = CircleInfo(data.get("object"))
			case _:self.object=None


class FeedsList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.feeds: list[Feed] = [Feed(feed) for feed in data.get("feed", [])]
		self.circleMap: list[Circle] = [Circle(circle) for circle in data.get("circleMap", {}).values()]
		self.hasMore: bool = data.get("hasMore")
