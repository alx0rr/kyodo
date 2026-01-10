


class BaseEvent:
	def __init__(self, data: dict, type: int):
		self.data: dict = data
		self.event_type = type