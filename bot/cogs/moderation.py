import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger
from core.repository import user_repo, mod_repo
from datetime import timedelta

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        # 1. Get user records (or create if missing)
        db_user = await user_repo.get_by_discord_id(str(member.id))
        if not db_user:
            db_user = await user_repo.create({"discord_id": str(member.id), "username": member.name})
        
        db_moderator = await user_repo.get_by_discord_id(str(interaction.user.id))
        
        # 2. Log to DB
        await mod_repo.create({
            "user_id": db_user["id"],
            "action": "WARN",
            "reason": reason,
            "moderator_id": db_moderator["id"] if db_moderator else None
        })
        
        await interaction.response.send_message(f"⚠️ {member.mention} has been warned. Reason: {reason}")
        logger.info(f"User {member.id} warned by {interaction.user.id}: {reason}")

    @app_commands.command(name="mute", description="Mute a user (Timeout)")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration_minutes: int, reason: str):
        duration = timedelta(minutes=duration_minutes)
        await member.timeout(duration, reason=reason)
        
        db_user = await user_repo.get_by_discord_id(str(member.id))
        db_moderator = await user_repo.get_by_discord_id(str(interaction.user.id))
        
        await mod_repo.create({
            "user_id": db_user["id"] if db_user else None,
            "action": "MUTE",
            "reason": f"Duration: {duration_minutes}m | Reason: {reason}",
            "moderator_id": db_moderator["id"] if db_moderator else None
        })
        
        await interaction.response.send_message(f"🔇 {member.mention} has been muted for {duration_minutes} minutes. Reason: {reason}")

    @app_commands.command(name="ban", description="Ban a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.ban(reason=reason)
        
        db_user = await user_repo.get_by_discord_id(str(member.id))
        db_moderator = await user_repo.get_by_discord_id(str(interaction.user.id))
        
        await mod_repo.create({
            "user_id": db_user["id"] if db_user else None,
            "action": "BAN",
            "reason": reason,
            "moderator_id": db_moderator["id"] if db_moderator else None
        })
        
        await interaction.response.send_message(f"🔨 {member.mention} has been banned. Reason: {reason}")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
