from discord.ext import commands
from tasks import setup_tasks


def setup_events(bot: commands.Bot, config: dict):

    @bot.event
    async def on_ready():
        setup_tasks(bot, config)

    @bot.event
    async def on_member_join(member):
        channel = bot.get_channel(int(config["CHANNEL_ID_YOUTUBE"]))
        if channel:
            await channel.send(f"¡Bienvenido al servidor, {member.mention}! 🎉")

    @bot.event
    async def on_member_remove(member):
        channel = bot.get_channel(int(config["ID_CHANNEL_REMOVE"]))
        if channel:
            await channel.send(f"{member} abandonó el servidor")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando no encontrado.")
