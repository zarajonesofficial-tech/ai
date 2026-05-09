import discord
from discord.ext import commands
from core.config import settings
from utils.logger import bot_logger

class ChrizAI(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        bot_logger.info("Setting up Discord Bot...")
        # Load Cogs
        await self.load_extension("bot.cogs.moderation")
        await self.load_extension("bot.cogs.operational")
        await self.load_extension("bot.cogs.tickets")
        await self.load_extension("bot.cogs.minecraft")
        await self.load_extension("bot.cogs.ai")
        
        # Sync slash commands
        if settings.GUILD_ID:
            guild = discord.Object(id=settings.GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()
        bot_logger.info("Slash commands synced.")

    async def on_ready(self):
        bot_logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        bot_logger.info("------")

bot = ChrizAI()

async def start_bot():
    try:
        if not settings.DISCORD_TOKEN or settings.DISCORD_TOKEN == "your_discord_bot_token":
            bot_logger.warning("DISCORD_TOKEN not set. Skipping bot startup.")
            return
        await bot.start(settings.DISCORD_TOKEN)
    except Exception as e:
        bot_logger.error(f"Failed to start Discord Bot: {e}")
