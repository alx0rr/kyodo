from .base import BaseClass
from ..objects import (
	MediaTarget, StickerPack,
	StickerInfo, StickerPackList
)
from ..utils import require_auth

from typing import IO
from _io import BufferedReader
from aiofiles.threadpool.binary import AsyncBufferedReader




class StickersModule(BaseClass):


	@require_auth
	async def get_my_sticker_packs(self, circleId: str, start: int = 0, limit: int = 25) -> StickerPackList:
		result = await self.req.make_async_request("GET", f"/{circleId}/s/stickers/packs?type=owned&limit={limit}&start={start}")
		return StickerPackList(await result.json())

	@require_auth
	async def get_sticker_pack_info(self, packId: str, start: int = 0, limit: int = 15) -> StickerPack:
		result = await self.req.make_async_request("GET", f"/g/s/stickers/packs/{packId}?limit={limit}&start={start}")
		StickerPack(await result.json())

	@require_auth
	async def add_sticker(self, packId: str, image: IO | BufferedReader | AsyncBufferedReader) -> StickerInfo:
		sticker_data = await self.upload_media(image, MediaTarget.StickerImage)
		result = await self.req.make_async_request("POST", f"/g/s/stickers?pack_id={packId}", {
			"resource": sticker_data.url
		})
		data: dict = await result.json()
		return StickerInfo(data["sticker"])