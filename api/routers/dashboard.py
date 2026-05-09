from typing import Optional

import discord
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from bot.main import bot
from core.config import settings

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


class MessageActionRequest(BaseModel):
    channel_id: int = Field(..., description="Discord text channel ID")
    content: str = Field(..., min_length=1, max_length=2000)
    mention_everyone: bool = False
    mention_here: bool = False
    pin_message: bool = False


def verify_internal_api_key(x_internal_api_key: Optional[str]) -> None:
    if not settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=503, detail="INTERNAL_API_KEY is not configured.")
    if x_internal_api_key != settings.INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid internal API key.")


def get_control_guild() -> discord.Guild:
    if not settings.GUILD_ID:
        raise HTTPException(status_code=503, detail="GUILD_ID is not configured.")

    guild = bot.get_guild(settings.GUILD_ID)
    if not guild:
        raise HTTPException(status_code=503, detail="Bot is not ready or guild is unavailable.")
    return guild


@router.get("/channels")
async def list_channels(x_internal_api_key: Optional[str] = Header(default=None)):
    verify_internal_api_key(x_internal_api_key)
    guild = get_control_guild()

    channels = [
        {"id": channel.id, "name": channel.name}
        for channel in guild.text_channels
        if channel.permissions_for(guild.me).send_messages
    ]
    return {"guild_id": guild.id, "channels": channels}


@router.post("/message")
async def send_dashboard_message(
    payload: MessageActionRequest,
    x_internal_api_key: Optional[str] = Header(default=None),
):
    verify_internal_api_key(x_internal_api_key)

    channel = bot.get_channel(payload.channel_id)
    if not channel:
        try:
            channel = await bot.fetch_channel(payload.channel_id)
        except Exception as exc:
            raise HTTPException(status_code=404, detail=f"Channel not found: {exc}") from exc

    if not isinstance(channel, discord.TextChannel):
        raise HTTPException(status_code=400, detail="Target channel must be a text channel.")

    if not channel.permissions_for(channel.guild.me).send_messages:
        raise HTTPException(status_code=403, detail="Bot cannot send messages in this channel.")

    content = payload.content.strip()
    if payload.mention_everyone:
        content = f"@everyone {content}"
    elif payload.mention_here:
        content = f"@here {content}"

    allowed_mentions = discord.AllowedMentions(
        everyone=payload.mention_everyone or payload.mention_here,
        roles=True,
        users=True,
    )

    try:
        sent_message = await channel.send(content, allowed_mentions=allowed_mentions)
        if payload.pin_message:
            if not channel.permissions_for(channel.guild.me).manage_messages:
                raise HTTPException(status_code=403, detail="Bot cannot pin messages in this channel.")
            await sent_message.pin(reason="Pinned from CHRIZ__3656 AI dashboard")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {exc}") from exc

    return {
        "ok": True,
        "message_id": sent_message.id,
        "channel_id": channel.id,
        "jump_url": sent_message.jump_url,
        "pinned": payload.pin_message,
    }
