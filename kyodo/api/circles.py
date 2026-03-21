from .base import BaseClass
from ..utils import require_auth

from kyodo.objects import Circle, CircleInfo

class CircleModule(BaseClass):

	@require_auth
	async def get_joined_circles(self) -> list[Circle]:
		response = await self.req.make_async_request("GET", "/g/s/circles/joined")
		return [Circle(x) for x in (await response.json()).get("circleList")]
		

	@require_auth
	async def get_circle_info(self, circleId: str) -> CircleInfo:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles")
		return CircleInfo(await response.json())
		
	@require_auth
	async def get_circle_description(self, circleId: str) -> str:
		response = await self.req.make_async_request("GET", f"/{circleId}/s/circles/description")
		return (await response.json()).get("description", '')
	
	@require_auth
	async def join_circle(self, circleId: str) -> CircleInfo:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/join")
		return CircleInfo(await response.json())

	@require_auth
	async def leave_circle(self, circleId: str) -> CircleInfo:
		response = await self.req.make_async_request("POST", f"/{circleId}/s/circles/leave")
		return CircleInfo(await response.json())