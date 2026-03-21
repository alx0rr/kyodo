


class StickerInfo:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data
		self.stickerId: str = data.get("id")
		self.packId: str = data.get("packId")
		self.name: str | None = data.get("name")
		self.url: str = data.get("resource")
		self.isCustom: bool = data.get("isCustom")
		self.position: int = data.get("position")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")
		self.updatedTime: str = data.get("updatedTime")