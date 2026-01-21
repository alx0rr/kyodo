from . import Circle


class MetaCircle:
	def __init__(self, data: dict):
		self.data: dict = data
		self.id: str = data.get("id")
		self.vanity: str = data.get("id")
		self.icon: str = data.get("icon")
		self.banner: str = data.get("banner")
		self.name: str = data.get("name")
		self.language: str = data.get("language")
		self.theme: dict = data.get("theme")
		self.moduleTypes: dict = data.get("moduleTypes")

		self.privacy: int = data.get("privacy")
		self.status: int = data.get("status")
		self.dau: int = data.get("dau")
		self.createdTime: str = data.get("createdTime")



class HomefeedExploreModule:
	def __init__(self, data: dict):
		self.data: dict = data
		self.id: str = data.get("id")
		self.type: int = data.get("type")
		self.queryType: int = data.get("queryType")
		self.title: str = data.get("title")
		self.counter: int = data.get("counter")
		self.createdTime: str = data.get("createdTime")
		self.itemList: list[Circle] = [Circle(circle) for circle in data.get("itemList", [])]
		

class HomefeedExplore:
	def __init__(self, data: dict):
		self.data: dict = data
		self.language: str = data.get("language")
		self.languages: list[str] = data.get("languages")
		bannerMeta: dict = data.get("bannerMeta", {})
		self.bannerMetaImage: str = bannerMeta.get("image")
		self.bannerMetaCircle: MetaCircle = MetaCircle(bannerMeta.get("circle"))
		self.modules: list[HomefeedExploreModule] = list()
		

		for module in data.get("modules", []):
			if module.get("type") == 0:
				self.modules.append(
					HomefeedExploreModule(module)
				)