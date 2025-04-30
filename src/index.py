import discord
from discord.ext import commands
from dotenv import dotenv_values
from commands import setup_commands
from events import setup_events
from help import HelpCommand

config = dotenv_values("../.env")
TOKEN = config["TOKEN_BOT_DISCORD"]
CHANNEL_ID = config["CHANNEL_ID_JOIN"]
ID_CHANNEL_REMOVE = config["ID_CHANNEL_REMOVE"]

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guild_messages = True
intents.guilds = True
intents.members = True

bot: commands.Bot = commands.Bot(
    command_prefix="-", intents=intents, help_command=HelpCommand()
)

setup_commands(bot, config)
setup_events(bot, config)


bot.run(TOKEN)
