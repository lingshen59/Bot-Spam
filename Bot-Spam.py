import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# hola
load_dotenv()

# IDs
GUILDS_RESTRINGIDAS = list(map(int, os.getenv("GUILDS_RESTRINGIDAS").split(',')))
CANAL_AUTORIZADOS_ID = int(os.getenv("CANAL_AUTORIZADOS_ID"))
CANAL_LOGS_ID = int(os.getenv("CANAL_LOGS_ID"))
GUILD_ID = int(os.getenv("GUILD_ID"))
usuarios_autorizados = []

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True  
        intents.message_content = True      
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
   
    embed = discord.Embed(
        title="Members Authorized's",
        color=discord.Color.blue()
    )
    if usuarios_autorizados:
        for user in usuarios_autorizados:
            embed.add_field(name="\u200b", value=f"{user.mention}", inline=False)
    else:
        embed.description = "No hay usuarios autorizados aún."
    
    async for message in canal_autorizados.history(limit=10):
        if message.author == bot.user:
            await message.edit(embed=embed)
            return
   
    await canal_autorizados.send(embed=embed)

@bot.tree.command(name="spam", description="Spam")
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
   
    num_respuestas = 5  
    intervalo_ms = 200  
    intervalo = intervalo_ms / 1000.0
    
    embed = discord.Embed(
        title="⸸                SERVER SPAMMED BY INFERNUMSQUAD                ⸸",
        description="# SERVER SPAMMED BY InfernumSquad)",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="\u200b", value="‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ─────────✦─────────‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ", inline=False) 
    embed.set_footer(text="InfernumSquad")
    embed.set_image(url="https://media.discordapp.net/attachments/1235744013236043888/1253141256947761232/a_b91b0a63867f80ab6995a61b45642af4-0374F.gif?ex=67a6a23d&is=67a550bd&hm=05a9f1298fec5e9472ab15b1c11361290caa28faa50d9bc1e185a2dfd4595711&")  # Cambia esto por la URL de tu imagen. Si quieres dejalo asi🤑🤑

    await interaction.response.send_message(".", ephemeral=True)
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  
        await interaction.followup.send(
            content="# @everyone https://discord.gg/infernumsquad", 
            embed=embed, 
            ephemeral=False
        )

@bot.tree.command(name="spamcustom", description="Spamcustom")
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

    num_respuestas = 10  
    intervalo_ms = 200   
    intervalo = intervalo_ms / 1000.0
  
    await interaction.response.send_message(
        ".", ephemeral=True
    )
  
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)
        await interaction.followup.send(
            f"{texto}", ephemeral=False
        )
        
@bot.tree.command(name="spamembed", description="Crea un embed personalizado.")
async def spamembed(interaction: discord.Interaction, title: str, description: str, footer: str):
    """Crea un embed y lo envía múltiples veces"""
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
        
    num_respuestas = 5  
    intervalo_ms = 100  

   
    intervalo = intervalo_ms / 1000.0  

  
    await interaction.response.send_message(".", ephemeral=True)

 
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    embed.set_footer(text=footer)


    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)  # Esperar el intervalo configurado
        await interaction.followup.send(embed=embed, ephemeral=False)

@bot.event
async def on_command(ctx):
    await enviar_logs_command(ctx)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
