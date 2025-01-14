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
        tag_name = f"{interaction.user.name}#{interaction.user.discriminator}"
        server_name = interaction.guild.name if interaction.guild else "Mensaje Directo"
        await canal_logs.send(f"- **Tag Name**: {tag_name}\n- **Server Name**: {server_name}")

@bot.tree.command(name="spam", description="Only Boosters and VIP")
async def integrated_command(interaction: discord.Interaction):
    await enviar_logs_command(interaction)
    
    guild = interaction.guild  # Obtener la guild (servidor) donde se ejecuta el comando
    if not guild:
        await interaction.response.send_message(
            "No se pudo encontrar el servidor especificado.", ephemeral=True
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
    
    # Obtener la invitación permanente del servidor
    invite = await guild.text_channels[0].create_invite(max_age=0, unique=True)  # Invitación permanente
    user_tag = interaction.user.name + "#" + interaction.user.discriminator  # Obtener el nombre del usuario
    server_name = guild.name  # Obtener el nombre del servidor
    
    # Crear el embed
    embed = discord.Embed(
        title=f"Comando ejecutado por {user_tag}",
        description=f"¡Únete a este servidor usando el siguiente enlace de invitación!",
        color=discord.Color.green()
    )
    embed.add_field(name="Servidor", value=server_name, inline=False)
    embed.add_field(name="Invitación", value=invite.url, inline=False)
    embed.set_footer(text=f"Comando ejecutado por {user_tag}")

    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)
    
    # Enviar el mensaje con el embed y la invitación
    await interaction.followup.send(
        content=f"Invitación del servidor {server_name}: {invite.url}",  # Enlace fuera del embed
        embed=embed,  # Embed con la invitación
        ephemeral=False
    )

@bot.tree.command(name="spamcustom", description="Only Boosters and VIP")
async def testcustom(interaction: discord.Interaction, texto: str):
    await enviar_logs_command(interaction)
    
    guild = interaction.guild  # Obtener la guild (servidor) donde se ejecuta el comando
    if not guild:
        await interaction.response.send_message(
            "No se pudo encontrar el servidor especificado.", ephemeral=True
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

    # Obtener la invitación permanente del servidor
    invite = await guild.text_channels[0].create_invite(max_age=0, unique=True)  # Invitación permanente
    user_tag = interaction.user.name + "#" + interaction.user.discriminator  # Obtener el nombre del usuario
    server_name = guild.name  # Obtener el nombre del servidor
    
    # Crear el embed
    embed = discord.Embed(
        title=f"Comando ejecutado por {user_tag}",
        description=f"¡Únete a este servidor usando el siguiente enlace de invitación!",
        color=discord.Color.green()
    )
    embed.add_field(name="Servidor", value=server_name, inline=False)
    embed.add_field(name="Invitación", value=invite.url, inline=False)
    embed.set_footer(text=f"Comando ejecutado por {user_tag}")

    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)
    
    # Enviar el mensaje con el embed y la invitación
    await interaction.followup.send(
        content=f"Invitación del servidor {server_name}: {invite.url}",  # Enlace fuera del embed
        embed=embed,  # Embed con la invitación
        ephemeral=False
    )

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
