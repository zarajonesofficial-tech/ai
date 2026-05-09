import discord
import datetime
import utils.logger
from discord import app_commands
from discord.ext import commands
from ai.orchestrator.main import orchestrator
from ai.orchestrator.social_memory import social_memory
from core.repository import op_repo
from loguru import logger

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_cooldowns = {}
        self.is_throttled = False

    @app_commands.command(name="ai", description="Ask the CHRIZ__3656 AI a question")
    async def ai_ask(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer()
        try:
            # Pass full context to allow potential action execution
            response_content = await orchestrator.handle_query(
                message=question,
                member=interaction.user,
                channel=interaction.channel
            )
            
            embed = discord.Embed(
                title="AI Operational Assistant", 
                description=response_content, 
                color=discord.Color.blue()
            )
            embed.set_footer(text="Grounded in real-time server data.")
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.bind(module="BOT").error(f"AI command failed: {e}")
            await interaction.followup.send("❌ Sorry, I encountered an error.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return

        # 1. Passive observation
        await social_memory.add_message(
            channel_id=message.channel.id,
            role="user",
            content=message.content,
            author_name=message.author.display_name
        )

        # 2. Check triggers
        is_mentioned = self.bot.user.mentioned_in(message)
        is_reply_to_me = message.reference and message.reference.resolved and message.reference.resolved.author.id == self.bot.user.id

        if is_mentioned or is_reply_to_me:
            # 3. Cooldown (10 seconds)
            now = datetime.datetime.now()
            last_call = self.channel_cooldowns.get(message.channel.id)
            if last_call and (now - last_call).total_seconds() < 10:
                return
            self.channel_cooldowns[message.channel.id] = now

            try:
                # Trigger typing indicator once
                if not self.is_throttled:
                    try:
                        await message.channel.typing()
                    except discord.HTTPException as e:
                        if e.status == 429:
                            self.is_throttled = True
                            logger.bind(module="BOT").warning("Discord throttling detected.")
                
                clean_content = message.content.replace(f"<@{self.bot.user.id}>", "").replace(f"<@!{self.bot.user.id}>", "").strip()
                
                if not clean_content and is_mentioned:
                    await message.reply("Entha bro, njan ivide und 👀")
                    return

                # Master Pipeline: Automatically routes to Social, Action, or Factual
                response_content = await orchestrator.handle_query(
                    message=clean_content,
                    member=message.author,
                    channel=message.channel
                )
                
                await message.reply(response_content)
                self.is_throttled = False
                
            except discord.HTTPException as e:
                if e.status == 429:
                    self.is_throttled = True
                    logger.bind(module="BOT").warning(f"Throttled (429) in channel {message.channel.id}")
                else:
                    logger.bind(module="BOT").error(f"Discord HTTP Error: {e}")
            except Exception as e:
                logger.bind(module="BOT").error(f"AI Chat failed: {e}")

async def setup(bot):
    await bot.add_cog(AICog(bot))
