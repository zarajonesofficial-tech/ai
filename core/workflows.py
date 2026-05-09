import asyncio
from loguru import logger
from ai.manager import ai_manager
from core.repository import mod_repo, op_repo
from bot.main import bot as discord_bot
import discord

class AutonomousWorkflows:
    def __init__(self):
        self.incident_threshold = 5
        self.check_interval = 300 # 5 minutes

    async def monitor_moderation_spikes(self):
        """
        Detects a high volume of moderation actions and generates an AI summary.
        """
        while True:
            try:
                # 1. Fetch recent logs from last 5 mins (pseudo-logic for example)
                # In real implementation, filter by timestamp in SQL
                logs = await mod_repo.get_all()
                recent_logs = logs[-10:] # Last 10 for demo
                
                if len(recent_logs) >= self.incident_threshold:
                    logger.info("Moderation spike detected. Generating autonomous summary...")
                    
                    log_text = "\n".join([f"- {l['action']}: {l['reason']}" for l in recent_logs])
                    prompt = f"The following moderation actions occurred recently:\n{log_text}\n\nSummarize the incident and identify the main issue."
                    
                    summary = await ai_manager.generate_with_fallback(
                        messages=[{"role": "user", "content": prompt}],
                        system_prompt="You are an expert community safety analyst."
                    )
                    
                    # Notify Admins (Static channel ID for demo)
                    # channel = await discord_bot.fetch_channel(123456789)
                    # await channel.send(f"🚨 **Autonomous Incident Summary:**\n{summary.content}")
                
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Moderation monitor failed: {e}")
                await asyncio.sleep(60)

    async def monitor_server_health(self):
        """
        Proactively monitors Minecraft server status and drafts announcements if it goes down.
        """
        last_status = "online"
        while True:
            try:
                # In real implementation, use mc_client.run_command("list") or ping
                current_status = "online" # Placeholder
                
                if current_status == "offline" and last_status == "online":
                    logger.warning("Server went offline! Drafting announcement...")
                    prompt = "The Minecraft server has gone offline unexpectedly. Draft a calm and professional Discord announcement for the players."
                    announcement = await ai_manager.generate_with_fallback(
                        messages=[{"role": "user", "content": prompt}]
                    )
                    logger.info(f"Drafted Announcement: {announcement.content}")
                    # In real implementation: post to status channel
                
                last_status = current_status
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Health monitor failed: {e}")
                await asyncio.sleep(30)

workflows = AutonomousWorkflows()

async def start_workflows():
    asyncio.create_task(workflows.monitor_moderation_spikes())
    asyncio.create_task(workflows.monitor_server_health())
