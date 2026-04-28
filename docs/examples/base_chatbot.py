from kyodo import Client, ChatMessage, EventType 

client = Client()

@client.middleware(EventType.ChatMessage)
async def user_filter(message: ChatMessage):
    if message.author.userId == client.userId:return False


@client.command(["/help", "/commands"])
async def help_command(message: ChatMessage):
    await client.send_message(
        message.chatId,
        "📌 Available commands:\n"
        "/help — list of commands\n"
        "/ping — bot check",
        message.circleId
    )

@client.command(["/ping"])
async def ping_command(message: ChatMessage):
    await client.send_message(
        message.chatId,
        "🏓 pong",
        message.circleId,
        replyMessageId=message.messageId
    )


@client.event(EventType.ChatMemberJoin)
async def on_member_join(message: ChatMessage):
    await client.send_message(
        message.chatId,
        f"{message.author.nickname}, welcome to chat!",
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
