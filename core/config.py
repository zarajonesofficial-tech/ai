from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # General
    PROJECT_NAME: str = "CHRIZ__3656 AI"
    DEBUG: bool = True
    
    # Discord
    DISCORD_TOKEN: str
    GUILD_ID: Optional[int] = None
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # AI Provider
    AI_PRIMARY_PROVIDER: str = "groq"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Minecraft
    MC_HOST: Optional[str] = None
    MC_RCON_PORT: int = 25575
    MC_RCON_PASSWORD: Optional[str] = None
    
    # Automation
    PANEL_URL: Optional[str] = None
    PANEL_USER: Optional[str] = None
    PANEL_PASS: Optional[str] = None
    
    # Pterodactyl
    PTERO_API_KEY: Optional[str] = None
    PTERO_SERVER_ID: Optional[str] = None
    PTERO_PANEL_URL: str = "https://panel.wammuhost.com"
    
    # Official Bot API (for whitelist/dashboard integration)
    OFFICIAL_BOT_API: str = "https://skybot.skyrealm.fun"
    INTERNAL_API_KEY: Optional[str] = None
    
    # API
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
