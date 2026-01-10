


class StoreProduct:
	def __init__(self, data: dict):
		self.data: dict = data
		self.productId: str = data.get("id")
		self.type: int = data.get("type")
		self.icon: str = data.get("icon")
		self.resource: str | None = data.get("resource")
		self.name: str = data.get("name")
		self.price: str | None = data.get("price")
		self.theme: dict = data.get("theme")
		self.ownershipStatus: int = data.get("ownershipStatus")
		self.isNew: bool | None = data.get("isNew")
		self.createdTime: str = data.get("createdTime")

		self.version: int | None = data.get("version")
		self.status: int | None = data.get("status")
		self.content: str | None = data.get("content")
		self.isExclusive: bool | None = data.get("isExclusive")
		self.isFree: bool | None = data.get("isFree")
		self.availableCircleIds: list[str] | None = data.get("availableCircleIds")

class StoreProductsList:
	def __init__(self, data: dict):
		self.data: dict = data
		self.products: list[StoreProduct] = [StoreProduct(product) for product in data.get("products", [])]
		self.hasMore: bool = data.get("hasMore")
