from collections import deque
from typing import Dict, List
import asyncio

class SocialMemory:
    """
    A lightweight, in-memory store for recent chat context.
    Allows the AI to passively observe and hold natural conversations.
    Stores the last N messages per channel to keep the VPS resource usage low.
    """
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.channels: Dict[int, deque] = {}
        self.lock = asyncio.Lock()

    async def add_message(self, channel_id: int, role: str, content: str, author_name: str = None):
        """
        Adds a message to the rolling window for a specific channel.
        Prefixes user messages with their names to give the AI social context.
        """
        async with self.lock:
            if channel_id not in self.channels:
                self.channels[channel_id] = deque(maxlen=self.max_history)
            
            # Format user messages as "Username: Message" for better social understanding
            if role == "user" and author_name:
                display_content = f"{author_name}: {content}"
            else:
                display_content = content

            self.channels[channel_id].append({"role": role, "content": display_content})

    async def get_history(self, channel_id: int) -> List[Dict[str, str]]:
        """
        Retrieves the rolling history for a channel.
        Returns a list of messages compatible with AI provider interfaces.
        """
        async with self.lock:
            if channel_id in self.channels:
                return list(self.channels[channel_id])
            return []

    async def clear_history(self, channel_id: int):
        """Clears memory for a specific channel."""
        async with self.lock:
            if channel_id in self.channels:
                self.channels[channel_id].clear()

# Singleton instance for the platform
social_memory = SocialMemory()
