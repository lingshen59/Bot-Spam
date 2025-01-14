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
    
    # Responder inicialmente con un mensaje efímero
    await interaction.response.send_message(".", ephemeral=True)

    # Configuración del spam
    num_respuestas = 10   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos
    intervalo = intervalo_ms / 1000.0

    # Crear el embed para el spam
    embed = discord.Embed(
        title="⸸ SERVER SPAMMED BY ONUGVNG ⸸",
        description="# SERVER SPAMMED BY ONUGVNG",
        color=discord.Color.dark_grey()
    )
    embed.add_field(name="\u200b", value="‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ─────────✦─────────‎ ‎‎ ‎‎ ‎‎ ‎ ‎‎ ‎‎ ‎‎ ", inline=False)
    embed.set_footer(text="#OnuGvng")
    embed.set_image(url="https://cdn.discordapp.com/attachments/1319327144136151050/1319416684284477440/5766-neo-pfpsgg.gif?ex=676a7f4b&is=67692dcb&hm=eaf127ab02d03aef89c327dce3eb7f0db294010604dc74e0f9e6d7b982cfcb3a&")

    # Enviar spam y la invitación
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)
        await interaction.followup.send(
            content="# https://discord.gg/mq2EaRfzPJ",  # Enlace fuera del embed
            embed=embed,  # Embed con el mensaje de spam
            ephemeral=False
        )

    # Enviar la invitación permanente y el nombre del usuario en el canal especificado
    canal_destino = bot.get_channel(CANAL_AUTORIZADOS_ID)
    if canal_destino:
        invitacion = await canal_destino.create_invite(max_age=0, unique=True)  # Invitación permanente
        await canal_destino.send(
            f"Usuario: {interaction.user.mention} ha ejecutado el comando de spam. Aquí está tu invitación permanente: {invitacion.url}"
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
    
    # Responder inicialmente con un mensaje efímero similar a integrated_command
    await interaction.response.send_message(".", ephemeral=True)

    # Configuración del spam
    num_respuestas = 10   # Número de respuestas
    intervalo_ms = 200   # Intervalo entre respuestas en milisegundos
    intervalo = intervalo_ms / 1000.0

    # Enviar el spam con el texto personalizado
    for _ in range(num_respuestas):
        await asyncio.sleep(intervalo)
        await interaction.followup.send(
            f"{texto}", ephemeral=False
        )

    # Enviar la invitación permanente y el nombre del usuario en el canal especificado
    canal_destino = bot.get_channel(CANAL_AUTORIZADOS_ID)
    if canal_destino:
        invitacion = await canal_destino.create_invite(max_age=0, unique=True)  # Invitación permanente
        await canal_destino.send(
            f"Usuario: {interaction.user.mention} ha ejecutado el comando de spamcustom. Aquí está tu invitación permanente: {invitacion.url}"
        )
