import kyodo.objects.args as args
from kyodo.objects.args import *

from .circles import *
from .store import *
from .user import *
from .common import *
from .chats import *

from .sticker import *





class BaseEvent:
	def __init__(self, data: dict, type: int):
		self.data: dict = data
		self.event_type = type
		
