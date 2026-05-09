import discord
from discord import app_commands
from discord.ext import commands
from utils.minecraft import mc_client
from loguru import logger

class MinecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mc-command", description="Run a console command on the Minecraft server")
    @app_commands.checks.has_permissions(administrator=True)
    async def run_cmd(self, interaction: discord.Interaction, command: str):
        await interaction.response.defer()
        response = await mc_client.run_command(command)
        
        if response and len(response) > 1900:
            response = response[:1900] + "..."
            
        await interaction.followup.send(f"**Command:** `{command}`\n**Response:**\n```\n{response or 'No response'}\n```")

    @app_commands.command(name="players", description="List online players on the Minecraft server")
    async def list_players(self, interaction: discord.Interaction):
        await interaction.response.defer()
        response = await mc_client.run_command("list")
        await interaction.followup.send(f"🎮 **Online Players:**\n{response or 'Unable to fetch player list.'}")

async def setup(bot):
    await bot.add_cog(MinecraftCog(bot))
