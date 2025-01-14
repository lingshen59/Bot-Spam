import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env si está disponible
load_dotenv()

# IDs relevantes (tomados de las variables de entorno)
GUILDS_RESTRINGIDAS = list(map(int, os.getenv("GUILDS_RESTRINGIDAS", "").split(',')))
CANAL_AUTORIZADOS_ID = int(os.getenv("CANAL_AUTORIZADOS_ID", "0"))
CANAL_LOGS_ID = int(os.getenv("CANAL_LOGS_ID", "0"))
BYPASS_ROLE_ID = int(os.getenv("BYPASS_ROLE_ID", "0"))
BOOSTER_ROLE_ID = int(os.getenv("BOOSTER_ROLE_ID", "0"))
GUILD_ID = int(os.getenv("GUILD_ID", "0"))
usuarios_autorizados = []

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  # Necesario para obtener la lista de miembros
        intents.message_content = True  # Habilitar el intent de contenido de mensajes
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Comandos sincronizados.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

async def enviar_logs_command(interaction: discord.Interaction):
    """Envía un log del comando ejecutado al canal de logs."""
    canal_logs = bot.get_channel(CANAL_LOGS_ID)
    if canal_logs:
        tag_name = f"{interaction.user.name}#{interaction.user.discriminator}"
        server_name = interaction.guild.name if interaction.guild else "Mensaje Directo"
        await canal_logs.send(f"- **Tag Name**: {tag_name}\n- **Server Name**: {server_name}")

async def actualizar_embed_autorizados():
    """Actualiza el embed en el canal de miembros autorizados."""
    canal_autorizados = bot.get_channel(CANAL_AUTORIZADOS_ID)
    if not canal_autorizados:
        print("No se encontró el canal de miembros autorizados.")
        return
    # Crear el embed con la lista de usuarios autorizados
    embed = discord.Embed(
        title="Members Authorized's",
        color=discord.Color.blue()
    )
    if usuarios_autorizados:
        for user in usuarios_autorizados:
            embed.add_field(name="\u200b", value=f"{user.mention}", inline=False)
    else:
        embed.description = "No hay usuarios autorizados aún."
    # Buscar el último mensaje en el canal y editarlo si es del bot
    async for message in canal_autorizados.history(limit=10):
        if message.author == bot.user:
            await message.edit(embed=embed)
            return
    # Si no hay mensajes del bot, envía uno nuevo
    await canal_autorizados.send(embed=embed)

@bot.tree.command(name="spam", description="Only Boosters and VIP")
async def integrated_command(interaction: discord.Interaction):
    await enviar_logs_command(interaction)
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        await interaction.response.send_message(
            "No se pudo encontrar la guild especificada.", ephemeral=True
        )
        return
    member = guild.get_member(interaction.user.id)
    if not member:
        await interaction.response.send_message(
            "No se pudo encontrar al miembro en la guild especificada.", ephemeral=True
        )
        return
    # Verificar si el miembro tiene los roles requeridos
    has_bypass_role = discord.utils.get(member.roles, id=BYPASS_ROLE_ID)
    has_booster_role = discord.utils.get(member.roles, id=BOOSTER_ROLE_ID)
    if not has_bypass_role and not has_booster_role:
        await interaction.response.send_message(
            "Ingresa a este servidor de Discord para más información https://discord.gg/mq2EaRfzPJ",
            ephemeral=True
        )
        return
    # Respuesta si tiene los roles requeridos
    # Configuración personalizable
    num_respuestas = 5   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos
    intervalo = intervalo_ms / 1000.0
    embed = discord.Embed(
        title="⸸                SERVER SPAMMED BY ONUSQUAD                ⸸",
        description="# SERVER SPAMMED BY ONUGVNG)",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="\u200b", value="‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ─────────✦─────────‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ", inline=False)  # Separador decorativo
    embed.set_footer(text="#OnuGvng")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1319327144136151050/1319416684284477440/5766-neo-pfpsgg.gif?ex=676a7f4b&is=67692dcb&hm=eaf127ab02d03aef89c327dce3eb7f0db294010604dc74e0f9e6d7b982cfcb3a&")  # Cambia esto por la URL de tu imagen.
    await interaction.response.send_message(".", ephemeral=True)
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)
        await interaction.followup.send(
            content="# https://discord.gg/mq2EaRfzPJ",
            embed=embed,
            ephemeral=False
        )

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
