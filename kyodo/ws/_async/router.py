from kyodo.objects.resp import WSChatMessage
from kyodo.ws.router import Router
from typing import Callable

class AsyncRouter(Router):


    @staticmethod
    def command_validator(commands: list[str], handler: Callable):
        async def wrapped_handler(data: WSChatMessage):
            if not isinstance(data.message.content, str):
                return
            message_content = data.message.content.lower()
            for command in commands:
                if message_content.startswith(command.lower()):
                    data.message.content = data.message.content[len(command):].strip()
                    await handler(data)
                    break
        return wrapped_handler


    def __init__(self):
        super().__init__()