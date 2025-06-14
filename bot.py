import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_PANEL_CHANNEL_ID = 1382780571729526864  # ID, wo das Panel gepostet wird
CATEGORY_ID = 1383527821758169128  # Kategorie-ID, wo Tickets erstellt werden

# Rollen-IDs für den Zugriff (ersetze durch deine echten IDs)
ROLE_TEAMLEITUNG = 1383087980201119754
ROLE_FRAKTION = 1383086757083353178
ROLE_SUPPORT = 1383080677414535219

@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")

@bot.command()
async def ticketpanel(ctx):
    if ctx.channel.id != TICKET_PANEL_CHANNEL_ID:
        await ctx.send("Dieser Befehl kann nur im Ticket-Panel-Channel verwendet werden.")
        return

    embed = discord.Embed(
        title="🎫 Ticket Panel",
        description="Wähle deine Ticketart aus:",
        color=0xFF0000
    )

    class TicketView(discord.ui.View):
        @discord.ui.button(label="Teamleitung Ticket", style=discord.ButtonStyle.red)
        async def teamleitung_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await create_ticket(interaction, "teamleitung", ROLE_TEAMLEITUNG)

        @discord.ui.button(label="Fraktion Ticket", style=discord.ButtonStyle.red)
        async def fraktion_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await create_ticket(interaction, "fraktion", ROLE_FRAKTION)

        @discord.ui.button(label="Support Ticket", style=discord.ButtonStyle.red)
        async def support_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await create_ticket(interaction, "support", ROLE_SUPPORT)

    await ctx.send(embed=embed, view=TicketView())

async def create_ticket(interaction: discord.Interaction, ticket_type: str, role_id: int):
    guild = interaction.guild
    category = guild.get_channel(CATEGORY_ID)
    role = guild.get_role(role_id)
    if category is None or role is None:
        await interaction.response.send_message("Kategorie oder Rolle nicht gefunden!", ephemeral=True)
        return

    # Channel-Namen erstellen
    channel_name = f"ticket-{ticket_type}-{interaction.user.name}".lower()

    # Check ob Ticket-Channel schon existiert
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        await interaction.response.send_message(f"Du hast bereits ein {ticket_type}-Ticket: {existing_channel.mention}", ephemeral=True)
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    ticket_channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
    await ticket_channel.send(f"{interaction.user.mention} Dein {ticket_type}-Ticket wurde erstellt!")

    await interaction.response.send_message(f"Ticket erstellt: {ticket_channel.mention}", ephemeral=True)

token = os.getenv('MTM4MzQzMTIzMDc4MzIyOTk2Mw.GaNZmH.gJpPVpmS8z0F3cINRGFeYnn4NNjm49KUEBGg78')
bot.run(token)
