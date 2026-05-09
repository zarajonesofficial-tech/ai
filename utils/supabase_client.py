from supabase import create_client, Client
from core.config import settings
from loguru import logger

def get_supabase() -> Client:
    """
    Initializes and returns a Supabase client.
    """
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return supabase
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        raise

supabase = get_supabase()
