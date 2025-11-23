from . import BaseProfile

class Track:
	def __init__(self, data: dict = {}):
		self.data: dict = data
		self.trackId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")
		self.targetCount: int = data.get("targetCount")
		self.openedCount: int = data.get("openedCount")
		self.objectType: int = data.get("objectType")
		self.objectId: str = data.get("objectId")
		self.objectTitle: str = data.get("objectTitle")
		self.objectImage: str = data.get("objectImage")
		self.status: str = data.get("status")
		self.approvalStatus: str = data.get("approvalStatus")
		self.isTest: bool = data.get("isTest")
		self.testUid: str = data.get("testUid")
		self.url: str = data.get("url")
		self.content: str = data.get("content")
		self.language: str = data.get("language")
		self.targetTime: str = data.get("targetTime")
		self.createdTime: str = data.get("createdTime")
		self.updatedTime: str = data.get("updatedTime")
		self.op: BaseProfile = BaseProfile(data.get("op", {}))

class BroadcastsList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.tracks: list[Track] = [Track(track) for track in data.get("tracks", [])]
		self.hasMore: bool = data.get("hasMore")

