from kyodo import Client, EventType, ChatMessage, ChatType

client = Client()

AUTO_REPLY_TEXT = (
    "Sorry, I'm not available right now.\n"
    "I will reply later."
)


@client.middleware(EventType.ChatMessage)
async def user_filter(message: ChatMessage):
    if message.author.userId == client.userId:
        return False

@client.event(EventType.ChatTextMessage)
async def auto_reply(message: ChatMessage):
    chat_info = await client.get_chat_info(
        message.chatId,
        message.circleId
    )

    if chat_info.type != ChatType.PRIVATE:
        return

    await client.send_message(
        message.chatId,
        AUTO_REPLY_TEXT,
        message.circleId,
        replyMessageId=message.messageId
    )

async def main():
    await client.login("EMAIL", "PASSWORD")
    #await client.login_token("TOKEN")
    await client.socket_wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
