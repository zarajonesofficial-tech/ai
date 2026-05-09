import httpx
from typing import Dict, Any, Optional
from core.config import settings
from utils.logger import core_logger

class PterodactylClient:
    """
    Client for interacting with the Pterodactyl Panel API.
    Ported from the official Sky Bot Node.js logic.
    """
    def __init__(self):
        self.api_key = settings.PTERO_API_KEY
        self.server_id = settings.PTERO_SERVER_ID
        self.panel_url = settings.PTERO_PANEL_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "CHRIZ__3656 AI / 1.0.0"
        }

    async def send_power_signal(self, signal: str) -> bool:
        """
        Sends a power signal (start, stop, restart, kill) to the server.
        """
        if not self.api_key or not self.server_id:
            core_logger.warning("Pterodactyl API Key or Server ID not configured.")
            return False

        url = f"{self.panel_url}/api/client/servers/{self.server_id}/power"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json={"signal": signal}, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                return True
        except Exception as e:
            core_logger.error(f"Pterodactyl power signal '{signal}' failed: {e}")
            return False

    async def get_resources(self) -> Optional[Dict[str, Any]]:
        """
        Fetches real-time CPU, RAM, and Disk usage from the panel.
        """
        if not self.api_key or not self.server_id:
            return None

        url = f"{self.panel_url}/api/client/servers/{self.server_id}/resources"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                return data.get("attributes", {}).get("resources")
        except Exception as e:
            core_logger.warning(f"Failed to fetch Pterodactyl resources: {e}")
            return None

ptero_client = PterodactylClient()
