import discord
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values("../.env")
TOKEN = config["TOKEN_BOT_DISCORD"]

intents = discord.Intents.default()
intents.message_content = True

bot: commands.Bot = commands.Bot(command_prefix="-", intents=intents)


@bot.event
async def on_ready():
    print("We are running!")


# @bot.event
# async def on_member_join(member):
#     channel = bot.get_channel(YOUR_CHANNEL_ID)
#     if channel:
#         await channel.send(f'¡Bienvenido al servidor, {member.mention}! 🎉')


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


bot.run(TOKEN)
