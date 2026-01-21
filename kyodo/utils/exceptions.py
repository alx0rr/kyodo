from orjson import JSONDecodeError
from kyodo.utils.request_helper import AsyncHTTPResponse



class KyodoError(Exception):
	"""
	Base class for all kyodo-related errors.
	"""
	def __init__(self, message: str | None = None, response: AsyncHTTPResponse | None = None):
		self.response: AsyncHTTPResponse | None = response
		self.message: str | None = message
		super().__init__(message or response or '')



class LibraryError(Exception):
	"""
	Base class for all library-related errors.
	"""
	def __init__(self, message: str | None = None, response: AsyncHTTPResponse | None = None):
		self.response: AsyncHTTPResponse | None = response
		self.message: str | None = message
		super().__init__(message or response or '')





class UnknownError(LibraryError):
	"""
	An unknown error occurred.
	"""

class NeedAuthError(LibraryError):
	"""
	Called when an attempt is made to perform an action that requires authorization.
	"""


class UnsupportedArgumentType(LibraryError):
	"""
	Called when you pass an unsupported argument type.
	"""


class UnsupportedFileType(LibraryError):
	"""
	Called when you pass an unsupported file type.
	"""

class ArgumentNeeded(LibraryError):
	"""
	Called when no arguments are passed or a required argument is missing.
	"""

class NoDataError(LibraryError):
	"""
	Called when the final data for a request is empty (all arguments are None).
	"""





class NotFoundError(KyodoError):
	"""
	Called if the resource is not found.
	"""


class ForbiddenError(KyodoError):
	"""
	Called when the server denies an action.
	"""


class TooManyRequestsError(KyodoError):
	"""
	Called when you send too many requests in a short period of time (just put a sleep for 2 seconds)
	"""


class AccessRestricted(KyodoError):
	"""
	Called when there is insufficient permission to execute the request.
	"""


class VersionOutOfDate(KyodoError):
	"""
	Called when an invalid request is sent. Often associated with incorrect data or updating security systems in the application.
	"""

class AuthError(KyodoError):
	"""
	Called when an authorization error occurs.
	"""


errors = {
	"0:404": NotFoundError,
	"0:403": ForbiddenError,
	"0:401": AuthError,
	"0:419": AccessRestricted,
	"0:429": TooManyRequestsError,
	"0:453": VersionOutOfDate
}

async def checkException(response: AsyncHTTPResponse):
	try:
		data: dict = await response.json()
		apiCode = data.get("apiCode")
		code = data.get("code")
		message = data.get("message")
		_ = f"{apiCode}:{code}"
	except JSONDecodeError:
		raise UnknownError(await response.text(), response)
	if _ in errors: raise errors[_](message, response)
	else:raise UnknownError(message, response)