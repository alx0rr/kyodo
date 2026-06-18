from __future__ import annotations
from orjson import JSONDecodeError
from kyodo.utils.request_helper import AsyncHTTPResponse, HTTPRequest, HTTPResponse
from kyodo.utils.constants import BUG_REPORT_URL
from kyodo.utils.generators import decode_auth_token


import traceback


class KyodoError(Exception):
	"""
	Base class for all kyodo-related errors.
	"""

	BUG_REPORT_HINT = (
		f"Found a bug? Use error.format_report() to generate a report, "
		f"then paste it here: {BUG_REPORT_URL}"
	)

	def __init__(
		self,
		message: str | None = None,
		response: AsyncHTTPResponse | None = None,
	):
		self.response: AsyncHTTPResponse | None = response
		self.request: HTTPRequest | None = response.request if response else None
		self.message: str | None = message
		super().__init__(message or response or "")

	def __str__(self) -> str:
		base = self.message or str(self.response) or ""
		return f"{base}\n\n{self.BUG_REPORT_HINT}" if base else self.BUG_REPORT_HINT

	def format_report(self, extra: str | None = None) -> str:
		"""
		Generate a pre-formatted bug report to paste into a GitHub issue.

		Example:
			try:
				await client.do_something()
			except exceptions.KyodoError as e:
				print(e.format_report())
				# or with extra context:
				print(e.format_report(extra="Happens only on startup"))
		"""

		tb = "".join(traceback.format_tb(self.__traceback__)) if self.__traceback__ else None
		lines = [
			"## Bug Report ",
			f"**Error type:** `{type(self).__name__}`",
			f"**Message:** {self.message or '—'}",
		]

		if self.request:
			lines += [
				"## Request",
				f"**Method:** `{self.request.method}`",
				f"**URL:** `{self.request.url}`",

			]

			if self.request.headers:
				headers = dict(self.request.headers)

				if headers.get("device-id"):
					headers["device-id"] = "[redacted]"

				if headers.get("Authorization"):
					token_info = decode_auth_token(headers["Authorization"])
					headers["Authorization"] = (
						f"[redacted] (exp={token_info.exp})"
					)
				formatted = "',\n".join(str(headers).split("',"))

				msg = f"```\n{formatted}\n```"
				lines += [
					"### Headers",
					msg,
				]

		if self.response:
			lines += [
				"## Response",
				f"**Status:** `{self.response.status}`",
			]

		if tb:
			lines += [
				"## Traceback",
				f"```\n{tb}\n```",
			]

		if extra:
			lines += ["## Additional Info", extra]

		return "\n\n".join(lines)



class LibraryError(Exception):
	"""
	Base class for all library-related errors.
	"""
	def __init__(self, message: str | None = None, response: AsyncHTTPResponse | None = None):
		self.response: AsyncHTTPResponse | None = response
		self.request: HTTPRequest | None = response.request if response else None
		self.message: str | None = message
		super().__init__(message or response or '')


class UnknownError(LibraryError):
	"""
	An unknown error occurred.
	"""

class NeedAuthError(LibraryError):
	"""
	Raised when an attempt is made to perform an action that requires authorization.
	"""


class UnsupportedArgumentType(LibraryError):
	"""
	Raised when you pass an unsupported argument type.
	"""


class UnsupportedFileType(LibraryError):
	"""
	Raised when you pass an unsupported file type.
	"""

class ArgumentNeeded(LibraryError):
	"""
	Raised when no arguments are passed or a required argument is missing.
	"""

class NoDataError(LibraryError):
	"""
	Raised when the final data for a request is empty (all arguments are None).
	"""

class ContentTypeError(LibraryError):
	"""
	ContentType found is not valid.
	"""


class BadArgument(LibraryError):
	"""
	Raised when you pass an unsupported argument type.
	"""

class NotFoundError(KyodoError):
	"""
	Raised if the resource is not found.
	"""

class DoesNotExistAnymore(KyodoError):
	"""
	Raised if the resource does not exist anymore.
	"""

class ForbiddenError(KyodoError):
	"""
	Raised when the server denies an action.
	"""


class TooManyRequestsError(KyodoError):
	"""
	Raised when you send too many requests in a short period of time (just put a sleep for 2 seconds)
	"""


class AccessRestricted(KyodoError):
	"""
	Raised when there is insufficient permission to execute the request.
	"""


class VersionOutOfDate(KyodoError):
	"""
	Raised when an invalid request is sent. Often associated with incorrect data or updating security systems in the application.
	"""

class AuthError(KyodoError):
	"""
	Raised when an authorization error occurs.
	"""

class SessionExpired(KyodoError):
	"""
	Raised when an session expired.
	"""






class EmailInUse(KyodoError):
    """Raised when the provided email address is already registered to an existing account."""

class IncorrectCredentials(KyodoError):
    """Raised when the login attempt fails due to a wrong email or password."""

class CircleDoesNotExist(KyodoError):
    """Raised when the requested circle could not be found (deleted or invalid ID)."""

class InvalidUsername(KyodoError):
    """Raised when the username does not meet the platform's format or length requirements."""

class UsernameTaken(KyodoError):
    """Raised when the chosen username is already taken by another account."""

class InvalidAccount(KyodoError):
    """Raised when the account is missing, banned, or otherwise not accessible."""



errors = {
	"0:404": NotFoundError,
	"0:403": ForbiddenError,
	"0:401": AuthError,
	"0:419": AccessRestricted,
	"0:429": TooManyRequestsError,
	"0:453": VersionOutOfDate,
	"0:498": SessionExpired,
	"1005:404": DoesNotExistAnymore,
	"1006:406": AccessRestricted,
	"2014:400": IncorrectCredentials,
	"2001:400": EmailInUse,
	"2007:400": InvalidUsername,
	"2010:400": UsernameTaken,
	"2022:400": InvalidAccount,
	"5000:404": CircleDoesNotExist,
	"5021:406": AccessRestricted,
	
}

async def checkAsyncException(response: AsyncHTTPResponse):
	try:
		data: dict = await response.json()
		apiCode = data.get("apiCode", "0")
		code = data.get("code")
		message = data.get("message")
		_ = f"{apiCode}:{code}"
	except JSONDecodeError:
		raise UnknownError(await response.text(), response)
	if _ in errors: raise errors[_](message, response)
	else:raise UnknownError(f"[{_}]: {message}", response)



def checkException(response: HTTPResponse):
	try:
		data: dict = response.json()
		apiCode = data.get("apiCode", "0")
		code = data.get("code")
		message = data.get("message")
		_ = f"{apiCode}:{code}"
	except JSONDecodeError:
		raise UnknownError(response.text(), response)
	if _ in errors: raise errors[_](message, response)
	else:raise UnknownError(f"[{_}]: {message}", response)