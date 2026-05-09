import discord
from discord import app_commands
from discord.ext import commands
from core.repository import user_repo, ticket_repo
from ai.orchestrator.main import orchestrator
from loguru import logger

class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Open a support ticket")
    async def create_ticket(self, interaction: discord.Interaction, reason: str):
        # 1. Create ticket channel
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites,
            category=None 
        )
        
        # 2. Log to DB
        db_user = await user_repo.get_by_discord_id(str(interaction.user.id))
        if not db_user:
            db_user = await user_repo.create({"discord_id": str(interaction.user.id), "username": interaction.user.name})
            
        ticket = await ticket_repo.create({
            "user_id": db_user["id"],
            "status": "open",
            "summary": reason
        })
        
        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)
        
        # 3. AI Initial Greeting & Search
        await channel.send(f"👋 Hello {interaction.user.mention}! I'm the CHRIZ__3656 AI assistant. I'm reviewing your issue: **{reason}**")
        
        # Use Orchestrator for factual response
        response_content = await orchestrator.handle_query(reason)
        
        await channel.send(response_content)
        await channel.send("\n*If this didn't resolve your issue, please wait for a moderator to assist you.*")

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))
