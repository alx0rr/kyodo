"""
Unofficial Kyodo API Library


### This is an ***unofficial*** Python library for interacting with Kyodo's HTTPS API and WebSocket services.

The library provides a wide range of features, including:
- Full authentication and account management
- Real-time communication via WebSocket
- Tools for working with chats, circles, users, ect
- Moderation tools for administrators and community managers
- Post and folder management
- Common utility endpoints and data fetching

Whether you're building a bot, automating tasks, or integrating Kyodo into your application, this library offers a high-level and convenient interface to work with all major features of the platform.

**Documentation:**  
- https://github.com/alx0rr/kyodo/blob/main/docs/index.md

Note: This library is not affiliated with or endorsed by Kyodo. Use it responsibly and at your own risk.
Note: This version of the library has been redesigned for public use to hide the secret keys for generating the request signature.
"""


from kyodo.utils import log, logging, exceptions
from kyodo.utils.requester import Requester

from kyodo.utils.generators import random_ascii_string as generate_deviceId
from kyodo.utils.generators import decode_auth_token

from kyodo.objects import *

from kyodo.ws import MiddlewareStopException
from kyodo.async_client import Client as AsyncClient
from kyodo.client import Client



def set_log_level(level = logging.INFO):
	"""
	Sets the logging level.

	:param level: The new logging level (e.g., logging.DEBUG, logging.ERROR).
	"""
	log.set_level(level)


def enable_file_logging(log_file: str = 'kyodo.log'):
	"""
	Enables logging to a file.

	:param log_file: The file where logs will be written.
	"""
	log.enable_file_logging(log_file)


def disable_file_logging():
	"""
	Disables logging to a file.
	"""
	if log.log_to_file:
		log.log_to_file = False
		log.logger.removeHandler(log.logger.handlers[-1])



__version__ = '1.6'
__newest__ = __version__
__title__ = 'kyodo'
__author__ = 'alx0rr'
__license__ = 'MIT'
__copyright__ = f'Copyright 2025-2026 {__author__}'

__link__ = "https://t.me/Alx0rrHub"
__project_link__ = 'https://pypi.org/pypi/kyodo'


from httpx import get
from packaging.version import parse as parse_version


try:
	response = get(f"{__project_link__}/json", timeout=3)
	data = response.json()
	__newest__ = data.get("info", {}).get("version", __version__)
except Exception:pass


def check_lib_version():
	current = parse_version(__version__)
	newest = parse_version(__newest__)

	if newest > current:
		log.warning(
			f'{__title__} made by {__author__}\n'
			f'Please update the library.\n'
			f'Your version: {current}  Latest version: {newest}\n'
			f'Follow our projects and updates: {__link__}'
		)


if __name__ != "__main__":
	check_lib_version()