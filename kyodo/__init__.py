"""
Unofficial Kyodo API Library

An unofficial Python library for interacting with Kyodo's HTTPS API and WebSocket services.

Features:
- Full authentication and account management
- Real-time communication via WebSocket
- Tools for working with chats, circles, users, etc.
- Moderation tools for administrators and community managers
- Post and folder management
- Common utility endpoints and data fetching

Docs: https://github.com/alx0rr/kyodo/blob/main/docs/index.md

Note: This library is not affiliated with or endorsed by Kyodo. Use responsibly and at your own risk.
Note: Redesigned for public use — secret keys for request signature generation are not exposed.
"""

from __future__ import annotations

# Utilities: device ID generator and auth token decoder
from kyodo.utils.generators import random_ascii_string as generate_deviceId
from kyodo.utils.generators import decode_auth_token  # usage: decode_auth_token(client.token)

# Argument and response objects (avoids magic numbers/strings in API calls)
from kyodo.objects import args
from kyodo.objects import resp

# Exceptions
from kyodo.utils import exceptions
from kyodo.ws import MiddlewareStopException

# Logging
from kyodo.utils import log
from kyodo.utils.logger import loglevel, Logger

# Event routers — sync and async variants
from kyodo.ws.router import Router
from kyodo.ws._async.router import AsyncRouter

# Clients — sync and async variants
from kyodo.async_client import Client as AsyncClient
from kyodo.client import Client


def set_log_level(level: int | str = loglevel.INFO):
    """
    Set the global logging level.

    :param level: Logging level (e.g. loglevel.DEBUG, loglevel.INFO, loglevel.DISABLE).
    """
    log.set_level(level)


def enable_file_logging(log_file: str = 'kyodo.log'):
    """
    Enable logging output to a file.

    :param log_file: Path to the log file. Defaults to 'kyodo.log'.
    """
    log.enable_file_logging(log_file)


def disable_file_logging():
    """
    Disable logging output to a file and remove the file handler.
    """
    if log.log_to_file:
        log.log_to_file = False
        log.logger.removeHandler(log.logger.handlers[-1])



__version__ = '2.0.0'
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
except Exception:
    pass 


def check_lib_version():
    """
    Warn the user if the installed library version is outdated.
    Compares the current version against the latest release on PyPI.
    """
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