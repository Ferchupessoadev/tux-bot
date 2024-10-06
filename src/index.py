import discord
from discord.ext import commands
from dotenv import dotenv_values
from commands import setup_commands
from events import setup_events

config = dotenv_values("../.env")
TOKEN = config["TOKEN_BOT_DISCORD"]
CHANNEL_ID = config["CHANNEL_ID_JOIN"]
ID_CHANNEL_REMOVE = config["ID_CHANNEL_REMOVE"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot: commands.Bot = commands.Bot(command_prefix="-", intents=intents)

setup_commands(bot)
setup_events(bot, config)


bot.run(TOKEN)
