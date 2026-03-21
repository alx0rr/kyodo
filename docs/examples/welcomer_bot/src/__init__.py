from kyodo import Client, set_log_level
from config import deviceId, log_level

set_log_level(log_level)
client = Client(deviceId)




from .join_handler import _