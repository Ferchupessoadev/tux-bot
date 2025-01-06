import discord.ext.commands as commands
import discord


class HelpCommand(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        help_message = "━━━━━━━━━━━━━━━━━━━━━━━\n"

        for cog, commands in mapping.items():
            if cog:
                help_message += f"\n**{cog.qualified_name}**:\n"
            for command in commands:
                help_message += f"`-{command.name}` - {command.help}\n"

        help_message += "━━━━━━━━━━━━━━━━━━━━━━━\n"

        embed = discord.Embed(
            title=":bar_chart: Comandos disponibles",
            color=discord.Color.blue(),
            description=help_message,
        )

        embed.set_thumbnail(url=self.context.bot.user.avatar.url)

        await self.context.send(embed=embed)
        await self.context.send("para obtener ayuda de un comando, escriba `-help [comando]`")

    async def send_cog_help(self, cog):
        pass

    async def command_not_found(self, string):
        await self.get_destination().send(f"Comando no encontrado: {string}")

    async def send_command_help(self, command):
        help_message = f"**{command.name}**: {command.help}"
        await self.get_destination().send(help_message)
