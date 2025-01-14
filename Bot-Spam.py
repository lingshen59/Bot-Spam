import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# IDs relevantes
GUILDS_RESTRINGIDAS = list(map(int, os.getenv("GUILDS_RESTRINGIDAS").split(',')))
CANAL_AUTORIZADOS_ID = int(os.getenv("CANAL_AUTORIZADOS_ID"))
CANAL_LOGS_ID = int(os.getenv("CANAL_LOGS_ID"))
BYPASS_ROLE_ID = int(os.getenv("BYPASS_ROLE_ID"))
BOOSTER_ROLE_ID = int(os.getenv("BOOSTER_ROLE_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))
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
    """Envia un log del comando ejecutado al canal de logs."""
    canal_logs = bot.get_channel(CANAL_LOGS_ID)
    if canal_logs:
        try:
            guild = interaction.guild
            user = interaction.user
            # Crear una invitación permanente en el primer canal de texto
            invite = await guild.text_channels[0].create_invite(max_age=0, unique=True)
            log_message = (
                f"**Comando ejecutado por**: {user.name}#{user.discriminator}\n"
                f"**Servidor**: {guild.name}\n"
                f"**Invitación**: {invite.url}"
            )
            # Enviar el log al canal de logs
            await canal_logs.send(log_message)
            print(f"Invitación enviada al canal de logs: {log_message}")
        except Exception as e:
            print(f"Error al crear o enviar invitación: {e}")
    else:
        print("No se encontró el canal de logs.")

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
    num_respuestas = 10   # Número de respuestas
    intervalo_ms = 200    # Intervalo entre respuestas en milisegundos
    intervalo = intervalo_ms / 1000.0  # Convertir milisegundos a segundos

    embed = discord.Embed(
        title="⸸ SERVER SPAMMED BY ONUGVNG ⸸",
        description="# SERVER SPAMMED BY ONUGVNG)",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="\u200b", value="‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ─────────✦─────────‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ", inline=False)  # Separador decorativo
    embed.set_footer(text="#OnuGvng")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1319327144136151050/1319416684284477440/5766-neo-pfpsgg.gif?ex=676a7f4b&is=67692dcb&hm=eaf127ab02d03aef89c327dce3eb7f0db294010604dc74e0f9e6d7b982cfcb3a&")  # Cambia esto por la URL de tu imagen.

    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)

    # Enviar múltiples mensajes con el embed y el enlace en un solo mensaje
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(
            content="# https://discord.gg/mq2EaRfzPJ",  # Enlace fuera del embed
            embed=embed,  # Embed en el mismo mensaje
            ephemeral=False
        )

@bot.tree.command(name="spamcustom", description="Only Boosters and VIP")
async def testcustom(interaction: discord.Interaction, texto: str):
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
    # Configuración personalizable
    num_respuestas = 10   # Número de respuestas
    intervalo_ms = 200    # Intervalo entre respuestas en milisegundos
    intervalo = intervalo_ms / 1000.0  # Convertir milisegundos a segundos

    # Responder inicialmente con un mensaje efímero similar a integrated_command
    await interaction.response.send_message(".", ephemeral=True)

    # Enviar múltiples respuestas con el texto proporcionado
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)
        await interaction.followup.send(
            f"{texto}", ephemeral=False
        )

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
