from typing import List, Optional, Dict, Any
from utils.supabase_client import supabase
from loguru import logger

class BaseRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name

    async def get_all(self) -> List[Dict[str, Any]]:
        try:
            response = supabase.table(self.table_name).select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching all from {self.table_name}: {e}")
            return []

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table(self.table_name).select("*").eq("id", id).single().execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching {id} from {self.table_name}: {e}")
            return None

    async def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table(self.table_name).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating record in {self.table_name}: {e}")
            return None

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table(self.table_name).update(data).eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating record {id} in {self.table_name}: {e}")
            return None

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("users")

    async def get_by_discord_id(self, discord_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table(self.table_name).select("*").eq("discord_id", discord_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching user by discord_id {discord_id}: {e}")
            return None

class OperationalStateRepository(BaseRepository):
    def __init__(self):
        super().__init__("operational_state")

    async def get_latest(self) -> Optional[Dict[str, Any]]:
        try:
            response = supabase.table(self.table_name).select("*").order("updated_at", desc=True).limit(1).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching latest operational state: {e}")
            return None

class ModerationRepository(BaseRepository):
    def __init__(self):
        super().__init__("moderation_logs")

class TicketRepository(BaseRepository):
    def __init__(self):
        super().__init__("tickets")

user_repo = UserRepository()
op_repo = OperationalStateRepository()
mod_repo = ModerationRepository()
ticket_repo = TicketRepository()
