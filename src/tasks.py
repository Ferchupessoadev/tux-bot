from discord.ext import tasks


def setup_tasks(bot, config):
    @tasks.loop(seconds=30)
    async def send_message():
        channel = bot.get_channel(int(config["ID_CHANNEL_TEST"]))
        if channel:
            await channel.send("test -> tarea periodica")

    send_message.start()
