from mcp.server.fastmcp import FastMCP
from loguru import logger
from core.repository import op_repo, user_repo
from bot.main import bot as discord_bot
import discord

# Initialize FastMCP - The modern high-level API for MCP
mcp_app = FastMCP(
    "CHRIZ__3656 AI MCP Server",
    instructions="Modular AI-powered operations, automation, and community management platform."
)

@mcp_app.tool()
async def send_discord_message(channel_id: int, content: str) -> str:
    """Send a message to a specific Discord channel"""
    try:
        channel = discord_bot.get_channel(channel_id)
        if not channel:
            # Try fetching if not in cache
            channel = await discord_bot.fetch_channel(channel_id)
        
        if isinstance(channel, (discord.TextChannel, discord.Thread)):
            await channel.send(content)
            return f"Successfully sent message to channel {channel_id}"
        return f"Error: Channel {channel_id} is not a text channel."
    except Exception as e:
        logger.error(f"MCP tool send_discord_message failed: {e}")
        return f"Error sending message: {str(e)}"

@mcp_app.tool()
async def get_operational_state() -> dict:
    """Get the current status of the server and active events"""
    state = await op_repo.get_latest()
    if state:
        return state
    return {"error": "Operational state not found"}

@mcp_app.tool()
async def get_server_info() -> dict:
    """Get overall Discord server statistics (member count, channel count, etc.)"""
    guild = discord_bot.guilds[0] if discord_bot.guilds else None
    if not guild:
        return {"error": "Bot is not in any server."}
    
    return {
        "name": guild.name,
        "member_count": guild.member_count,
        "text_channels": len(guild.text_channels),
        "voice_channels": len(guild.voice_channels),
        "roles": [r.name for r in guild.roles if r.name != "@everyone"]
    }

@mcp_app.tool()
async def list_members(limit: int = 50) -> list:
    """Get a list of server members (names and IDs)"""
    guild = discord_bot.guilds[0] if discord_bot.guilds else None
    if not guild:
        return []
    
    return [{"name": m.name, "id": m.id, "display_name": m.display_name} for m in guild.members[:limit]]

@mcp_app.tool()
async def get_channel_history(channel_id: int, limit: int = 20) -> list:
    """Read previous messages from a specific channel to understand context"""
    try:
        channel = discord_bot.get_channel(channel_id) or await discord_bot.fetch_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return {"error": "Channel is not a text channel."}
        
        history = []
        async for msg in channel.history(limit=limit):
            history.append({
                "author": msg.author.name,
                "content": msg.content,
                "timestamp": str(msg.created_at)
            })
        return history
    except Exception as e:
        return {"error": str(e)}

@mcp_app.tool()
async def list_channels() -> list:
    """Get a list of all visible channels in the server"""
    guild = discord_bot.guilds[0] if discord_bot.guilds else None
    if not guild:
        return []
    
    return [{"name": c.name, "id": c.id, "type": str(c.type)} for c in guild.channels]
