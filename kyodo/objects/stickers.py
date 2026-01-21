


class StickerPackList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.stickerPacks: list[StickerPackInfo] = [StickerPackInfo(sticker_pack) for sticker_pack in data.get("packs", [])]
		self.hasMore: bool = data.get("hasMore")



class StickerPackInfo:
	def __init__(self, data: dict):
		self.data: dict = data
		self.packId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")
		self.ogPackId: str = data.get("ogId")
		self.ogCircleId: str = data.get("ogCircleId")
		self.ogUserId: str = data.get("ogUid")
		self.name: str = data.get("name")
		self.icon: str | None = data.get("icon")
		self.stickerCount: int = data.get("stickerCount")
		self.type: int = data.get("type")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")
		self.updatedTime: str = data.get("updatedTime")


class StickerPack:
	def __init__(self, data: dict):
		self.data: dict = data
		self.stickers: list[StickerInfo] = [StickerInfo(sticker) for sticker in data.get("stickers", [])]
		self.hasMore: bool = data.get("hasMore")
		self.packStatus: int = data.get("packStatus")
		self.packId: str = data.get("packId")



class StickerInfo:
	def __init__(self, data: dict):
		self.data: dict = data
		self.stickerId: str = data.get("id")
		self.packId: str = data.get("packId")
		self.name: str | None = data.get("name")
		self.url: str = data.get("resource")
		self.aspectRatio: str = data.get("aspectRatio")
		self.position: int = data.get("position")
		self.status: int = data.get("status")
		self.createdTime: str = data.get("createdTime")
		self.updatedTime: str = data.get("updatedTime")