


class Folder:
	def __init__(self, data: dict):
		self.data: dict = data
		self.folderId: str = data.get("id")
		self.circleId: str = data.get("circleId")
		self.userId: str = data.get("uid")
		self.folderName: str = data.get("name")
		self.postCount: int = data.get("postCount")
		self.createdTime: str = data.get("createdTime")
		self.updatedTime: str = data.get("updatedTime")


class FoldersList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.chats: list[Folder] = [Folder(folder) for folder in data.get("folders", [])]
		self.hasMore: bool = data.get("hasMore")