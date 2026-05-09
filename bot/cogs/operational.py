import discord
import re
import asyncio
from discord import app_commands
from discord.ext import commands, tasks
from core.repository import op_repo
from utils.minecraft import mc_client
from loguru import logger

class OperationalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_presence.start()

    def cog_unload(self):
        self.update_presence.cancel()

    @tasks.loop(seconds=60)
    async def update_presence(self):
        """Periodically updates the bot's Discord status based on server state."""
        await self.bot.wait_until_ready()
        
        try:
            state = await op_repo.get_latest()
            if not state:
                return

            if state["status"] == "maintenance":
                activity = discord.Activity(type=discord.ActivityType.watching, name="Maintenance active ⚠")
                status = discord.Status.dnd
            else:
                # Try to get real player count for status
                mc_resp = await mc_client.run_command("list")
                player_count = "0"
                if mc_resp and "Error" not in mc_resp:
                    match = re.search(r"(\d+)/\d+", mc_resp)
                    if match: 
                        player_count = match.group(1)

                activity = discord.Activity(
                    type=discord.ActivityType.playing, 
                    name=f"SkyRealms 🌌 {player_count} players"
                )
                status = discord.Status.online

            await self.bot.change_presence(status=status, activity=activity)
            
        except Exception as e:
            logger.bind(module="BOT").warning(f"Presence update failed: {e}")

    @app_commands.command(name="status", description="Check server operational status")
    async def status(self, interaction: discord.Interaction):
        state = await op_repo.get_latest()
        if not state:
            await interaction.response.send_message("❌ Operational state not found.")
            return

        embed = discord.Embed(
            title="Operational Status",
            color=discord.Color.green() if state["status"] == "online" else discord.Color.orange()
        )
        embed.add_field(name="Status", value=state["status"].upper(), inline=True)
        embed.add_field(name="Owner Available", value="✅ Yes" if state["owner_available"] else "❌ No", inline=True)
        
        events = state.get("active_events", [])
        events_str = "\n".join([f"• {e}" for e in events]) if events else "No active events."
        embed.add_field(name="Active Events", value=events_str, inline=False)
        
        embed.set_footer(text="CHRIZ__3656 AI • Real-time Awareness")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(OperationalCog(bot))
