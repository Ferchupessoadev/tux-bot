from discord.ext import commands
import utils
import discord
import sys


def setup_commands(bot: commands.Bot, config):
    @bot.command(help="Muestra la latencia del bot")
    async def ping(ctx):
        await ctx.send(f":ping_pong: **pong**: Latencia `{round(bot.latency * 1000)}ms`")

    @bot.command(help="Informacion del bot")
    async def neofetch(ctx):
        distribucion = utils.get_linux_distro()
        uptime = utils.get_uptime()

        description = f"""

        ━━━━━━━━━━━━━━━━━━━━━━━
        :robot: **Nombre:** `{bot.user.name}`
        :penguin: **Distribución:** `{distribucion}`
        :computer: **Host**: `{utils.get_username()}`@`{utils.get_hostname()}`
        :stopwatch: **Uptime:** `{uptime[0]}d {uptime[1]}h {uptime[2]}m {uptime[3]}s`
        :battery: **RAM**: `{utils.get_ram()}`
        :book: **Python**: `V{sys.version.split()[0]}`
        :books: **discord.py** `V{discord.__version__}`
        ━━━━━━━━━━━━━━━━━━━━━━━
        """
        embed = discord.Embed(
            title="Neofetch",
            description=description,
            color=discord.Color.green(),
        )

        embed.set_thumbnail(url=bot.user.avatar.url)

        await ctx.send(embed=embed)
