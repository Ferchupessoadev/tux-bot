from discord.ext import tasks
from utils_youtube import latest_video_link
import discord


def setup_tasks(bot, config):

    bot.latest_video_link = latest_video_link(bot, config)

    @tasks.loop(seconds=60)
    async def cron_job_youtube():
        channel = bot.get_channel(int(config["CHANNEL_ID_YOUTUBE_DISCORD"]))
        if not channel:
            return

        link = latest_video_link(bot, config)
        if not link:
            return

        if bot.latest_video_link is None:
            bot.latest_video_link = link
            return

        if link != bot.latest_video_link:
            bot.latest_video_link = link
            await channel.send(
                "@everyone\n"
                "**¡Hey! 🔥 Hay algo nuevo en el canal de YouTube. ¡No te lo pierdas!**\n"
                f"{link}"
            )

    @tasks.loop(minutes=5)
    async def update_stats():
        guild = bot.get_guild(1250455329578418209)
        if not guild:
            return

        channel = guild.get_channel(1465398474970370161)
        if not channel:
            return

        online_channel = guild.get_channel(1465398551122280518)
        if not online_channel:
            return

        total = guild.member_count
        online = sum(
            1 for m in guild.members
            if not m.bot and m.status != discord.Status.offline
        )

        if online_channel:
            await online_channel.edit(name=f"🟢 Online: {online}")

        if channel:
            await channel.edit(name=f"👥 Total: {total}")

    cron_job_youtube.start()
    update_stats.start()
