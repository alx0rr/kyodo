


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


class StickerList:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data

		self.pagination: dict = data.get("pagination", {})

		self.stickers: list[StickerInfo] = [StickerInfo(x) for x in data.get("stickerList", [])]



class StickerPackInfo:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data

		self.packId: str = data.get("id")
		self.ogId: str = data.get("ogId")
		self.userId: str = data.get("uid")
		self.name: str = data.get("name")
		self.icon: str | None = data.get("icon")
		self.stickerCount: int = data.get("stickerCount")
		self.type: int = data.get("type")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")
		self.modifiedTime: str = data.get("modifiedTime")


class StickerPackList:
	def __init__(self, data: dict):
		data = data or {}
		self.data: dict = data

		self.pagination: dict = data.get("pagination", {})

		self.stickerPacks: list[StickerPackInfo] = [StickerPackInfo(x) for x in data.get("stickerPackList", [])]
