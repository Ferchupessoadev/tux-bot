from discord.ext import tasks
from utils_youtube import fetch_latest_content


def setup_tasks(bot, config):
    bot.latest_video = fetch_latest_content(
        config["CHANNEL_ID_YOUTUBE"], config)

    @tasks.loop(seconds=50)
    async def cron_job_youtube():
        channel = bot.get_channel(int(config["ID_CHANNEL_REMOVE"]))

        await channel.send(bot.latest_video)
