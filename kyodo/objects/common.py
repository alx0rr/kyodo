from .circles import Circle
from dataclasses import dataclass, asdict
import jwt

@dataclass
class JWTPayload:
	auth_token: str | None = None
	id: str | None = None
	email: str | None = None
	role: int | None = None
	premium_type: int | None = None
	language: str | None = None
	is_staff_member: bool | None = None
	iat: int | None = None
	exp: int | None = None

	@classmethod
	def from_token(cls, token: str):
		data = jwt.decode(token, options={"verify_signature": False})
		return cls(**data)

	@property
	def data(self) -> dict:
		return asdict(self)

	def __getitem__(self, key):
		return self.data.get(key)


class LanguageInfo:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.code: str = data.get("id")
		self.title: str = data.get("title")

class AvailableLanguages:

	def __init__(self, data: dict):
		data = data or {}
		self.data=data

		self.language: str = data.get("language")
		self.contentRegion: str = data.get("contentRegion")
		self.languageList: list[LanguageInfo] = [LanguageInfo(x) for x in data.get("languageList", [])]







class ShareLinkObject:
	def __init__(self, data: dict):
		data = data or {}
		self.data=data

class ShareLink:
	def __init__(self, data: dict):
		self.data: dict = data
		share_link: dict = data.get("shareLink", {})

		self.objectPreview: ShareLinkObject = ShareLinkObject(data.get("objectPreview", {}))
		self.circle : Circle = Circle(data.get("circle", {}))

		self.id: str = share_link.get("id")
		self.circleId: str = share_link.get("circleId")
		self.objectId: str = share_link.get("objectId")
		self.objectType: int = share_link.get("objectType")