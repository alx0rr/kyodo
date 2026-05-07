from kyodo import EventType

class SocketActions:

    async def ws_send(self, data: str | dict | bytes): ...

    
    async def ws_typing(self, chatId: str, circleId: str | None = None):
        await self.ws_send({
            "o": EventType.Typing,
            "d": {
                "circleId": circleId,
                "chatId": chatId
            }
            })

    async def ws_typing_end(self, chatId: str, circleId: str | None = None):
        await self.ws_send({
            "o": EventType.TypingEnd,
            "d": {
                "circleId": circleId,
                "chatId": chatId
            }
            })
        
    
    async def ws_open_circle_screen(self, circleId: str):
        await self.ws_send({
            "o": EventType.OpenCircleScreen,
            "d": {
                "circleId": circleId,
            }
            })

    async def ws_close_circle_screen(self, circleId: str):
        await self.ws_send({
            "o": EventType.CloseCircleScreen,
            "d": {
                "circleId": circleId,
            }
            })