import aiorcon
from core.config import settings
from loguru import logger
from typing import Optional

class MinecraftClient:
    def __init__(self):
        self.host = settings.MC_HOST
        self.port = settings.MC_RCON_PORT
        self.password = settings.MC_RCON_PASSWORD

    async def run_command(self, command: str) -> Optional[str]:
        if not self.host or not self.password:
            logger.bind(module="MC").warning("Minecraft RCON not configured. Skipping command.")
            return "Error: Minecraft RCON not configured."
        
        try:
            rcon = await aiorcon.RCON.create(
                self.host, 
                self.port, 
                self.password,
                timeout=10
            )
            response = await rcon.execute(command)
            rcon.close()
            return response
        except Exception as e:
            # Downgrade to warning as it's common for servers to be offline
            logger.bind(module="MC").warning(f"Minecraft RCON unreachable ({self.host}): {str(e)}")
            return f"Error: Server connection refused."

mc_client = MinecraftClient()
