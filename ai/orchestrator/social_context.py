from typing import List, Dict, Any, Optional
import discord

class DiscordSocialContext:
    """
    A structured data package containing all social and environmental context
    from Discord, giving the AI complete situational awareness.
    """
    def __init__(self, message: discord.Message = None):
        self.guild = {}
        self.channel = {}
        self.author = {}
        self.message_data = {}
        self.reply_context = {}
        
        if message:
            self.build_from_discord(message)

    def build_from_discord(self, message: discord.Message):
        # 1. Guild Context
        if message.guild:
            self.guild = {
                "id": str(message.guild.id),
                "name": message.guild.name
            }
            
        # 2. Channel Context
        self.channel = {
            "id": str(message.channel.id),
            "name": message.channel.name if hasattr(message.channel, "name") else "DM",
            "type": str(message.channel.type),
            "category": message.channel.category.name if hasattr(message.channel, "category") and message.channel.category else "None"
        }
        
        # 3. Author Context
        if isinstance(message.author, discord.Member):
            self.author = {
                "id": str(message.author.id),
                "username": message.author.name,
                "display_name": message.author.display_name,
                "roles": [r.name for r in message.author.roles if r.name != "@everyone"],
                "permissions": {
                    "admin": message.author.guild_permissions.administrator,
                    "moderator": message.author.guild_permissions.manage_messages
                }
            }
        else:
            self.author = {
                "id": str(message.author.id),
                "username": message.author.name,
                "display_name": message.author.name,
                "roles": [],
                "permissions": {"admin": False, "moderator": False}
            }

        # 4. Message Context
        self.message_data = {
            "content": message.content,
            "mentions_bot": message.guild.me in message.mentions if message.guild else False,
            "is_reply": message.reference is not None
        }

        # 5. Reply Context
        if message.reference and message.reference.resolved and isinstance(message.reference.resolved, discord.Message):
            replied_msg = message.reference.resolved
            self.reply_context = {
                "reply_to_user": replied_msg.author.display_name,
                "reply_to_message": replied_msg.content[:200] # Truncate for token efficiency
            }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "guild": self.guild,
            "channel": self.channel,
            "author": self.author,
            "message": self.message_data,
            "reply_context": self.reply_context
        }
