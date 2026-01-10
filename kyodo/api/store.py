from .base import BaseClass
from ..objects import (
	StoreProductsList,
	ProductTypes, StoreProduct
)
from ..utils import require_auth




class StoreModule(BaseClass):

	@require_auth
	async def get_my_store_products(self, start: int = 0, limit: int = 4) -> StoreProductsList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/store/owned?limit={limit}&start={start}")
		return StoreProductsList(await result.json())


	@require_auth
	async def get_store_products(self, start: int = 0, limit: int = 15) -> StoreProductsList:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/store?limit={limit}&start={start}")
		return StoreProductsList(await result.json())

	@require_auth
	async def get_store_product_info(self, productId: str, productType: str = ProductTypes.AvatarFrame) -> StoreProduct | dict:
		result = await self.req.make_async_request("GET", f"/g/s/monetization/{productType}/{productId}")
		data: dict = await result.json()
		match productType:
			case ProductTypes.AvatarFrame:
				return StoreProduct(data["avatarFrame"])
			case _: return data