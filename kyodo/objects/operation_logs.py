from . import BaseProfile

class Log:
	def __init__(self, data: dict):
		self.data: dict = data
		self.logId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.objectType: int = data.get("objectType")
		self.objectId: str = data.get("objectId")
		self.operatorId: str = data.get("operatorId")
		self.operation: int = data.get("operation")
		self.textOperation: str = data.get("textOperation")
		self.level: int = data.get("level")
		self.content: str = data.get("content")
		self.contentEn: str = data.get("contentEn")
		self.appPath: str = data.get("appPath")
		self.createdTime: str = data.get("createdTime")
		self.operator: BaseProfile = BaseProfile(data.get("operator", {}))
		
class OperationLogs:
	def __init__(self, data: dict):
		self.data: dict = data
		self.hasMore: bool = data.get("hasMore")
		self.logs: list[Log] = [Log(l) for l in data.get("logs", [])]