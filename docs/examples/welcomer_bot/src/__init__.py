from kyodo import AsyncClient, set_log_level
from config import deviceId, log_level

set_log_level(log_level)
client = AsyncClient(deviceId)




from .join_handler import _