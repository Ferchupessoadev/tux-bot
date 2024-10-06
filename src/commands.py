import subprocess
from discord.ext import commands
from utils import get_linux_distro, get_uptime


def setup_commands(bot: commands.Bot):
    @bot.command()
    async def ping(ctx):
        await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

    @bot.command()
    async def neofetch(ctx):
        result = subprocess.run(
            ['free', '-m'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.split('\n')
        distro = get_linux_distro()
        days, hours, minutes, seconds = get_uptime()

        for line in lines:
            if 'Mem:' in line:
                parts = line.split()
                total, used, free = map(int, parts[1:4])
                await ctx.send(f'OS: {distro}\nRAM: {used}MB/{total}MB\nTiempo encendido: {days}d {hours}h {minutes}m {seconds}s')
