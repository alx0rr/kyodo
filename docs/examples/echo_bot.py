from kyodo import Client, EventType, ChatMessage

client = Client()

async def echo_handler(message: ChatMessage):
    if message.author.userId == client.userId: return
    await client.send_message(
        message.circleId,
        message.chatId,
        message.content
    )

client.add_handler(EventType.ChatTextMessage, echo_handler)

@client.event(EventType.ChatTextMessage)
async def echo_handler_decorator(message: ChatMessage):
    print(f"[LOG] {message.author.nickname}: {message.content}")

async def main():
    client.login("EMAIL", "PASSWORD")
    #client.login_token("TOKEN", "USERID")
    client.socket_wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
