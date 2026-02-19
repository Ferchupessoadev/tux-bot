from discord.ext import tasks
import discord
from utils_youtube import get_latest_video_link


def setup_tasks(bot, config):
    bot.last_video_link = None

    @tasks.loop(minutes=5)
    async def cron_job_youtube():
        channel = bot.get_channel(int(config["CHANNEL_ID_YOUTUBE_DISCORD"]))
        if not channel:
            return

        data, link = get_latest_video_link(bot, config)
        if not link or not data:
            return

        # Primera ejecución → solo guardamos
        if bot.last_video_link is None:
            bot.last_video_link = link
            return

        # Video nuevo
        if link != bot.last_video_link:
            bot.last_video_link = link
            await channel.send(
                "**¡Hey! 🔥 Hay algo nuevo en el canal de YouTube. ¡No te lo pierdas!**\n"
                "**🎥 Nuevo video:**\n"
                f"Titulo: {data['snippet']['title']}\n"
                "Tag: ||@everyone|| ||@here||\n\n"
                f"**[Haz click aquí para ver el video({link})**"
            )

    @cron_job_youtube.before_loop
    async def before_youtube():
        await bot.wait_until_ready()

    @tasks.loop(minutes=5)
    async def update_stats():
        guild = bot.get_guild(1250455329578418209)
        if not guild:
            return

        total_channel = guild.get_channel(1465398474970370161)
        online_channel = guild.get_channel(1465398551122280518)

        total = guild.member_count
        online = sum(
            1 for m in guild.members
            if not m.bot and m.status != discord.Status.offline
        )

        if online_channel:
            new_name = f"🟢 Online: {online}"
            if online_channel.name != new_name:
                await online_channel.edit(name=new_name)

        if total_channel:
            new_name = f"👥 Total: {total}"
            if total_channel.name != new_name:
                await total_channel.edit(name=new_name)

    @update_stats.before_loop
    async def before_stats():
        await bot.wait_until_ready()

    cron_job_youtube.start()
    update_stats.start()
