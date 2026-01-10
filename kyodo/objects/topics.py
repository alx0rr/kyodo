



class Topic:
	def __init__(self, data: dict):
		self.data: dict = data
		self.topicId: str = data.get("id")
		self.name: str = data.get("name")
		self.lowercase_name: str = data.get("lowercase")
		self.score: int = data.get("score")
		self.isOfficial: bool = data.get("official")
		self.fgColor: str = data.get("fgColor")
		self.bgColor: str = data.get("bgColor")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")
