from __future__ import annotations
from typing import TYPE_CHECKING
import os
import aiofiles
if TYPE_CHECKING:
	from kyodo import Client, AsyncClient

VALID_EXTENSIONS = {
	"jpg", "jpeg", "png", "gif",  								 # images
	"mp4", "mov", "avi", "mkv", "webm",                          # video
	"mp3", "ogg", "wav", "flac", "aac",                          # audio
}

class MediaData:
	"""Represents a media file fetched from a remote URL."""

	def __init__(self, url: str, client: Client):
		self.url = url
		self.ext = self._parse_ext(url)
		self._client = client
		self._file: bytes | None = None

	@staticmethod
	def _parse_ext(url: str) -> str | None:
		"""Extract and validate file extension from URL, ignoring query params."""
		clean = url.split("?")[0].split("#")[0]
		ext = clean.split(".")[-1].lower() if "." in clean else None
		return ext if ext in VALID_EXTENSIONS else None

	def get(self) -> None:
		"""Download the file and cache it in memory."""
		resp = self._client.req.make_request("GET", api=self.url)
		self._file = resp.get_bytes()

	def get_bytes(self) -> bytes:
		"""Return the file as bytes, downloading it first if not yet cached."""
		if self._file is None:
			self.get()
		return self._file

	def save(self, path: str = ".", filename: str = "file", ext: str | None = None) -> str:
		"""
		Save the file to disk.

		:param path: Directory to save into. Defaults to current directory.
		:param filename: File name without extension. Defaults to 'file'.
		:param ext: Override file extension. Defaults to extension parsed from URL.
		:return: Full path to the saved file.
		:raises ValueError: If no valid extension is available.
		"""
		if self._file is None:
			self.get()

		resolved_ext = ext or self.ext
		if not resolved_ext:
			raise ValueError(
				f"Could not determine a valid file extension from URL: {self.url}\n"
				f"Specify it manually via the 'ext' parameter."
			)

		
		clean_path = os.path.join(path.rstrip("/\\"), f"{filename}.{resolved_ext}")

		with open(clean_path, "wb") as f:
			f.write(self._file)
		return clean_path
	



class AsyncMediaData:
	"""Represents a media file fetched from a remote URL."""

	def __init__(self, url: str, client: AsyncClient):
		self.url = url
		self.ext = self._parse_ext(url)
		self._client = client
		self._file: bytes | None = None

	@staticmethod
	def _parse_ext(url: str) -> str | None:
		"""Extract and validate file extension from URL, ignoring query params."""
		clean = url.split("?")[0].split("#")[0]
		ext = clean.split(".")[-1].lower() if "." in clean else None
		return ext if ext in VALID_EXTENSIONS else None

	async def get(self) -> None:
		"""Download the file and cache it in memory."""
		resp = await self._client.req.make_async_request("GET", api=self.url)
		self._file = await resp.get_bytes()

	async def get_bytes(self) -> bytes:
		"""Return the file as bytes, downloading it first if not yet cached."""
		if self._file is None:
			await self.get()
		return self._file

	async def save(self, path: str = ".", filename: str = "file", ext: str | None = None) -> str:
		"""
		Save the file to disk.

		:param path: Directory to save into. Defaults to current directory.
		:param filename: File name without extension. Defaults to 'file'.
		:param ext: Override file extension. Defaults to extension parsed from URL.
		:return: Full path to the saved file.
		:raises ValueError: If no valid extension is available.
		"""
		if self._file is None:
			await self.get()

		resolved_ext = ext or self.ext
		if not resolved_ext:
			raise ValueError(
				f"Could not determine a valid file extension from URL: {self.url}\n"
				f"Specify it manually via the 'ext' parameter."
			)

		
		clean_path = os.path.join(path.rstrip("/\\"), f"{filename}.{resolved_ext}")

		async with aiofiles.open(clean_path, "wb") as f:
			async with aiofiles.open(clean_path, "wb") as f:
				await f.write(self._file)
		return clean_path