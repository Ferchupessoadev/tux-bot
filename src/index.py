import discord
import subprocess
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values("../.env")
TOKEN = config["TOKEN_BOT_DISCORD"]
CHANNEL_ID = config["CHANNEL_ID_JOIN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot: commands.Bot = commands.Bot(command_prefix="-", intents=intents)


@bot.event
async def on_ready():
    print("We are running!")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel:
        await channel.send(f'¡Bienvenido al servidor, {member.mention}! 🎉')


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command()
async def neofetch(ctx):
    result = subprocess.run(['free', '-m'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.split('\n')
    for line in lines:
        if 'Mem:' in line:
            parts = line.split()
            total, used, free = map(int, parts[1:4])
            await ctx.send(f'RAM: {used}MB/{total}MB')


bot.run(TOKEN)
