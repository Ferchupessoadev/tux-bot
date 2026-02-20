from discord.ext import commands
from tasks import setup_tasks
import aiohttp
import io
from PIL import Image, ImageDraw, ImageFont
import discord


def setup_events(bot: commands.Bot, config: dict):

    @bot.event
    async def on_ready():
        setup_tasks(bot, config)

    @bot.event
    async def on_member_join(member):
        channel = bot.get_channel(int(config["CHANNEL_ID_JOIN"]))
        if not channel:
            return

        role_name = config["ROLE_DEFAULT"]
        if not role_name:
            return

        role = discord.utils.get(member.guild.roles, name=role_name)
        if role:
            try:
                if role < member.guild.me.top_role:
                    await member.add_roles(role, reason="Rol automático al ingresar")
            except discord.Forbidden:
                pass
            except discord.HTTPException:
                pass

        background = Image.open("fondo-welcome.jpg").convert("RGBA")
        W, H = background.size

        # --- Descargar avatar de forma segura ---
        avatar_url = member.display_avatar.url

        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                avatar_bytes = await resp.read()

        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar = avatar.resize((2300, 2300))
        border_size = 14

        # --- Crear máscara circular ---
        mask = Image.new("L", avatar.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, *avatar.size), fill=255)
        avatar.putalpha(mask)
        border = Image.new(
            "RGBA",
            (avatar.width + 2*border_size, avatar.height + 2*border_size),
            (255, 255, 255, 255)
        )
        mask_border = Image.new("L", border.size, 0)
        ImageDraw.Draw(mask_border).ellipse((0, 0, *border.size), fill=255)
        border.putalpha(mask_border)
        border.paste(avatar, (border_size, border_size), avatar)
        avatar = border

        # --- Posicionar avatar ---
        avatar_x = (W - avatar.width) // 2
        avatar_y = (H - avatar.height) // 2
        background.paste(avatar, (avatar_x, avatar_y), avatar)

        description = (
            f"**Bienvenido {member.mention}**\n"
            f"Primero lo primero, lee las <#{config['ID_CHANNEL_RULES']}>\n\n"
            f"Si tienes alguna duda o sugerencia, escribe en <#{config['ID_CHANNEL_SUGGESTIONS']}>\n"
            f"¡Esperamos que disfrutes tu estadía!"
        )

        embed = discord.Embed(
            description=description,
            color=discord.Color.green()
        )

        with io.BytesIO() as image_binary:
            background = background.convert("RGB")
            background.save(image_binary, "JPEG", quality=75, optimize=True)
            image_binary.seek(0)

            file = discord.File(image_binary, filename="avatar.png")
            embed.set_image(url="attachment://avatar.png")

            embed.set_footer(
                text="Tux Bot • Ferchupessoadev",
                icon_url="https://raw.githubusercontent.com/Ferchupessoadev/tux-bot/refs/heads/main/tuxbot.png")

            await channel.send(
                content=f"**Bienvenido {member.mention}**",
                embed=embed,
                file=file
            )

    @bot.event
    async def on_member_remove(member):
        channel = bot.get_channel(int(config["ID_CHANNEL_REMOVE"]))
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        if channel:
            embed = discord.Embed(
                title="Miembro abandonado",
                description=f"{member.display_name} ha abandonado el servidor.",
                color=discord.Color.red()
            )
            embed.set_image(url=avatar_url)

            embed.set_footer(
                text="Tux Bot • Ferchupessoadev",
                icon_url="https://raw.githubusercontent.com/Ferchupessoadev/tux-bot/refs/heads/main/tuxbot.png")

            await channel.send(embed=embed)

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando no encontrado")
