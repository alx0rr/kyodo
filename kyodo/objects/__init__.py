from .args import *

from .circles import *
from .store import *
from .user import *
from .common import *
from .chats import *







class BaseEvent:
	def __init__(self, data: dict, type: int):
		self.data: dict = data
		self.event_type = type
		
