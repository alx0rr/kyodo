from kyodo import EventType

class SocketActions:

    def ws_send(self, data: str | dict | bytes): ...

    def ws_typing(self, chatId: str, circleId: str | None = None):
        self.ws_send({
            "o": EventType.Typing,
            "d": {
                "circleId": circleId,
                "chatId": chatId
            }
            })

    def ws_typing_end(self, chatId: str, circleId: str | None = None):
        self.ws_send({
            "o": EventType.TypingEnd,
            "d": {
                "circleId": circleId,
                "chatId": chatId
            }
            })
        
    
    def ws_open_circle_screen(self, circleId: str):
        self.ws_send({
            "o": EventType.OpenCircleScreen,
            "d": {
                "circleId": circleId,
            }
            })

    def ws_close_circle_screen(self, circleId: str):
        self.ws_send({
            "o": EventType.CloseCircleScreen,
            "d": {
                "circleId": circleId,
            }
            })