from kyodo import Client, EventType, ChatMessage, ChatType

client = Client()

AUTO_REPLY_TEXT = (
    "Sorry, I'm not available right now.\n"
    "I will reply later."
)

@client.event(EventType.ChatTextMessage)
async def auto_reply(message: ChatMessage):
    chat_info = await client.get_chat_info(
        message.circleId,
        message.chatId
    )

    if chat_info.type != ChatType.PRIVATE:
        return

    await client.send_message(
        message.circleId,
        message.chatId,
        AUTO_REPLY_TEXT,
        replyMessageId=message.messageId
    )

async def main():
    client.login("EMAIL", "PASSWORD")
    # client.login_token("TOKEN", "USER_ID")
    client.socket_wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
