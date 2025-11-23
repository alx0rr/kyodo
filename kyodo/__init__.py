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
- https://github.com/xXxCLOTIxXx/kyodo/blob/main/docs/index.md

Note: This library is not affiliated with or endorsed by Kyodo. Use it responsibly and at your own risk.
Note: This version of the library has been redesigned for public use to hide the secret keys for generating the request signature.
"""


from .utils import log, logging, exceptions
from kyodo.utils.requester import Requester
from .objects import *
from .client import Client


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



__title__ = 'kyodo'
__author__ = 'Xsarz & illusion1stj'
__license__ = 'MIT'
__copyright__ = f'Copyright 2025 {__author__}'
__version__ = '0.9'


from requests import get
try:__newest__ = get("https://pypi.org/pypi/kyodo/json").json().get("info", {}).get("version", __version__)
except:__newest__=__version__
if __version__ != __newest__:
	log.warning(f'{__title__} made by {__author__}. Please update the library. Your version: {__version__}  A new version: {__newest__}')

"""
#TODO
Client.highlight_post #not yet implemented in kyodo app
Client.upload_media #Fix image loading (add x-sig generation for media file data)
"""
