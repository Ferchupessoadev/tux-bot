from discord.ext import tasks
from utils_youtube import latest_video_link


def setup_tasks(bot, config):

    bot.latest_video_link = latest_video_link(bot, config)

    @tasks.loop(seconds=60)
    async def cron_job_youtube():
        link = latest_video_link(bot, config)

        channel = bot.get_channel(int(config["CHANNEL_ID_YOUTUBE_DISCORD"]))
        if channel and link != bot.latest_video_link:
            bot.latest_video_link = link
            await channel.send(f"""
            @here\n **Nuevo video de YouTube!** \n{link}
            """)

    cron_job_youtube.start()
