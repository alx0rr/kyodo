

class Service:
	def __init__(self, data: dict):
		self.data: dict = data
		self.name: str = data.get("service")
		self.statusCode: int = data.get("statusCode")
		self.message: str = data.get("message")

class HealthServices:
	def __init__(self, data: list):
		self.data: list = data
		self.services: list[Service] = list()
		for i in self.data:
			self.services.append(Service(i))