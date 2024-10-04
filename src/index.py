import discord
import subprocess
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values("../.env")
TOKEN = config["TOKEN_BOT_DISCORD"]
CHANNEL_ID = config["CHANNEL_ID_JOIN"]
ID_CHANNEL_REMOVE = config["ID_CHANNEL_REMOVE"]

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


def get_linux_distro():
    try:
        with open("/etc/os-release") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("PRETTY_NAME"):
                return line.split("=")[1].strip().replace('"', '')
    except FileNotFoundError:
        return "No se pudo determinar la distribución de Linux"


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])

    uptime_days = uptime_seconds // (24 * 3600)
    uptime_hours = (uptime_seconds % (24 * 3600)) // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    uptime_seconds = uptime_seconds % 60

    return int(uptime_days), int(uptime_hours), int(uptime_minutes), int(uptime_seconds)


@bot.command()
async def neofetch(ctx):
    result = subprocess.run(['free', '-m'], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.split('\n')
    distro = get_linux_distro()
    days, hours, minutes, seconds = get_uptime()
    for line in lines:
        if 'Mem:' in line:
            parts = line.split()
            total, used, free = map(int, parts[1:4])
            await ctx.send(f'OS: {distro}\nRAM: {used}MB/{total}MB\nTiempo encendido: {days}d {hours}h {minutes}m {seconds}s')


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(ID_CHANNEL_REMOVE))
    if channel:
        await channel.send(f'{member.mention} abandono el servidor')


bot.run(TOKEN)
