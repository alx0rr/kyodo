from kyodo.objects import ChatMessage
from kyodo.ws.router import Router
from typing import Callable

class AsyncRouter(Router):


    @staticmethod
    def command_validator(commands: list[str], handler: Callable):
        async def wrapped_handler(data: ChatMessage):
            if not isinstance(data.content, str):
                return
            message_content = data.content.lower()
            for command in commands:
                if message_content.startswith(command.lower()):
                    data.content = data.content[len(command):].strip()
                    await handler(data)
                    break
        return wrapped_handler


    def __init__(self):
        super().__init__()