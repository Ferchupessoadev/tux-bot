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

        background = Image.open("fondo-welcome.png").convert("RGBA")
        W, H = background.size

        font_title = ImageFont.truetype(
            "./fonts/FiraCodeNerdFont-Regular.ttf", 80)
        font_sub = ImageFont.truetype(
            "./fonts/FiraCodeNerdFont-Regular.ttf", 65)
        draw = ImageDraw.Draw(background)

        # --- Descargar avatar de forma segura ---
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as resp:
                avatar_bytes = await resp.read()

        avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA")
        avatar = avatar.resize((600, 600))

        # --- Crear máscara circular ---
        mask = Image.new("L", avatar.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, *avatar.size), fill=255)
        avatar.putalpha(mask)
        border_size = 10
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

        # --- Escribir textos ---
        text = "¡Bienvenid@!"
        text_member = f"{member.name}!"

        # -------- Título --------
        bbox = draw.textbbox((0, 0), text, font=font_title)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((W - text_w) / 2, H - text_h - 160),
                  text, font=font_title, fill="#E74C3C")

        # -------- Subtítulo --------
        bbox2 = draw.textbbox((0, 0), text_member, font=font_sub)
        sub_w, sub_h = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        draw.text(((W - sub_w) / 2, H - sub_h - 90),
                  text_member, font=font_sub, fill="#E74C3C")

        # --- Enviar imagen ---
        with io.BytesIO() as image_binary:
            background.save(image_binary, "PNG")
            image_binary.seek(0)
            await channel.send(
                content=f"¡Bienvenido/a {member.mention}! 🎉",
                file=discord.File(image_binary, "bienvenida.png")
            )

    @bot.event
    async def on_member_remove(member):
        channel = bot.get_channel(int(config["ID_CHANNEL_REMOVE"]))
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        if channel:
            embed = discord.Embed(
                title="Miembro abandonado",
                description=f"{member.name} ha abandonado el servidor.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=avatar_url)
            await channel.send(embed=embed)


    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando no encontrado.")
