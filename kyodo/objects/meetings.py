from . import BaseProfile


class MeetMatch:
	def __init__(self, data: dict):
		self.data: dict = data
		self.matchId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")
		self.content: str = data.get("content")
		self.freezeExpTime: str = data.get("freezeExpTime")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")
		self.matchId: str = data.get("id")
		self.user: BaseProfile = BaseProfile(data.get("user"))

		target: dict = data.get("target")
		self.targetUserId: str = target.get("uid")
		self.targetUser: str = target.get("user")
		self.targetTime: str = target.get("time")