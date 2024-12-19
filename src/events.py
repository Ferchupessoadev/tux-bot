from discord.ext import commands


def setup_events(bot: commands.Bot, config):
    @bot.event
    async def on_ready():
        print("We are running!")

    @bot.event
    async def on_member_join(member):
        channel = bot.get_channel(int(config["CHANNEL_ID_JOIN"]))
        if channel:
            await channel.send(f'¡Bienvenido al servidor, {member.mention}! 🎉')

    @bot.event
    async def on_member_remove(member):
        channel = bot.get_channel(int(config["ID_CHANNEL_REMOVE"]))
        if channel:
            await channel.send(f'{member} abandonó el servidor')
