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
        intents.message_content = True       # Habilitar el intent de contenido de mensajes
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
            "Ingresa a este servidor de Discord para más información https://discord.gg/yJYmDHpW5h",
            ephemeral=True
        )
        return
    # Respuesta si tiene los roles requeridos
    # Configuración personalizable
    num_respuestas = 5   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos
    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 1000.0
    # Crear el embed personalizado
    embed = discord.Embed(
        title="⸸                SERVER SPAMMED BY INFERNUMSQUAD                ⸸",
        description="# SERVER SPAMMED BY InfernumSquad)",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="\u200b", value="‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ─────────✦─────────‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ", inline=False)  # Separador decorativo
    embed.set_footer(text="InfernumSquad")
    embed.set_image(url="https://media.discordapp.net/attachments/1235744013236043888/1253141256947761232/a_b91b0a63867f80ab6995a61b45642af4-0374F.gif?ex=67a6a23d&is=67a550bd&hm=05a9f1298fec5e9472ab15b1c11361290caa28faa50d9bc1e185a2dfd4595711&")  # Cambia esto por la URL de tu imagen.
    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)
    # Enviar múltiples mensajes con el embed y el enlace en un solo mensaje
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(
            content="# @everyone https://discord.gg/infernumsquad",  # Enlace fuera del embed
            embed=embed,  # Embed en el mismo mensaje
            ephemeral=False
        )

@bot.tree.command(name="spamcustom", description="Only Boosters and VIP")
async def testcustom(interaction: discord.Interaction, texto: str):
    await enviar_logs_command(interaction)
    """Recibe texto del usuario y responde con ese mismo texto."""
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
            "Ingresa a este servidor de Discord para más información https://discord.gg/yJYmDHpW5h",
            ephemeral=True
        )
        return
    # Configuración personalizable
    num_respuestas = 10   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos
    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 1000.0
    # Responder inicialmente con un mensaje efímero similar a integrated_command
    await interaction.response.send_message(
        ".", ephemeral=True
    )
    # Enviar múltiples respuestas con el texto proporcionado
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)
        await interaction.followup.send(
            f"{texto}", ephemeral=False
        )
        
@bot.tree.command(name="spamembed", description="Crea un embed personalizado.")
async def spamembed(interaction: discord.Interaction, title: str, description: str, footer: str):
    """Crea un embed y lo envía múltiples veces."""
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

    # Verificar si el miembro tiene el rol requerido
    has_bypass_role = discord.utils.get(member.roles, id=BYPASS_ROLE_ID)

    if not has_bypass_role:
        await interaction.response.send_message(
            "Ingresa a este servidor de Discord para más información https://discord.gg/yJYmDHpW5h", ephemeral=True
        )
        return

    # Configuración personalizable
    num_respuestas = 5   # Número de respuestas por defecto
    intervalo_ms = 100   # Intervalo entre respuestas en milisegundos por defecto

    # Convertir milisegundos a segundos
    intervalo = intervalo_ms / 1000.0  

    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)

    # Crear el embed personalizado
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    embed.set_footer(text=footer)

    # Enviar múltiples mensajes con el embed
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="masspoll", description="Create multiple polls quickly (VIP only)")
async def mass_poll(
    interaction: discord.Interaction,
    question: str,
    option1: str,
    option2: str,
    option3: str,
    option4: str,
    amount: int = 5  # 默认发 5 个 Poll
):
    """快速发送多个 Poll（优化 Rate Limit）"""
    # 1. 检查权限（和你的代码一致）
    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(interaction.user.id)
    has_bypass_role = discord.utils.get(member.roles, id=BYPASS_ROLE_ID)
    
    if not has_bypass_role:
        await interaction.response.send_message("❌ No permission.", ephemeral=True)
        return

    # 2. 先回应，避免 interaction failed
    await interaction.response.send_message("🚀 Creating polls...", ephemeral=True)

    # 3. 用 Webhook 或 followup 发送多个 Poll
    for i in range(amount):
        embed = discord.Embed(title=f"📊 POLL {i+1}: {question}", color=0x00ff00)
        embed.add_field(name="InfernumSquad On Top", value=option1)
        embed.add_field(name="SPAMMED BY INFERNUMSQUAD", value=option2)
        embed.add_field(name="InfernumSquadIsHere", value=option3)
        embed.add_field(name="InfernumSquad On Top", value=option4)
        embed.add_field(name="SPAMMED BY INFERNUMSQUAD", value=option5)
        
        # 方法 1: followup.send（推荐）
        await interaction.followup.send(embed=embed, wait=False)
        
        # 方法 2: Webhook（更高频）
        # webhook = await interaction.channel.create_webhook(name="Poll Spammer")
        # await webhook.send(embed=embed)
        # await webhook.delete()
        
        await asyncio.sleep(0.8)  # 控制速度（0.8 秒/Poll）

@bot.event
async def on_command(ctx):
    await enviar_logs_command(ctx)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
