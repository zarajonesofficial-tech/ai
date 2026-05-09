import json
import discord
from typing import Dict, Any, Optional
from ai.manager import ai_manager
from ai.orchestrator.permission_validator import permission_validator
from ai.orchestrator.humanizer import humanizer
from utils.minecraft import mc_client
from utils.pterodactyl import ptero_client
from utils.logger import core_logger

class ActionExecutor:
    """
    Parses intent into executable tasks, validates permissions, 
    and interacts with Discord/Minecraft/DB/Pterodactyl/Official Bot.
    """

    SYSTEM_PROMPT = """
    You are an Action Parser. Extract the requested action and its parameters from the user's message.
    Respond ONLY with a JSON object.
    
    Supported Actions:
    - send_message(content: str)
    - mention_everyone()
    - mention_role(role_name: str)
    - warn_user(username: str, reason: str)
    - mute_user(username: str, duration_mins: int, reason: str)
    - restart_server()
    - maintenance_on()
    - maintenance_off()
    - mc_broadcast(message: str)
    - review_whitelist()
    
    Example: 'review the whitelist'
    Output: {"action": "review_whitelist", "params": {}}
    """

    async def execute(self, message: str, member: discord.Member, channel: discord.TextChannel) -> str:
        """The main entry point for action execution."""
        try:
            # 1. Parse Parameters
            parse_resp = await ai_manager.generate_with_fallback(
                messages=[{"role": "user", "content": message}],
                system_prompt=self.SYSTEM_PROMPT
            )
            
            # Clean JSON
            clean_json = parse_resp.content.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            action = data.get("action")
            params = data.get("params", {})

            # 2. Permission Check
            if not permission_validator.can_execute(action, member):
                return "❌ You don't have the required role to do that, bro."

            # 3. Action Mapping
            core_logger.info(f"Executing action: {action} with params {params}")
            
            result_msg = ""
            if action == "mention_everyone":
                await channel.send("@everyone AI alert activated! 🌌")
                result_msg = "Mentioned everyone as requested."
                
            elif action == "mute_user":
                target_name = params.get("username", "")
                result_msg = f"Attempting to mute {target_name}..."
                
            elif action == "restart_server":
                # Use official Pterodactyl Client API
                success = await ptero_client.send_power_signal("restart")
                if success:
                    result_msg = "Restart signal sent to Pterodactyl panel successfully."
                else:
                    await mc_client.run_command("stop")
                    result_msg = "Pterodactyl failed, fallback restart sent via RCON."

            elif action == "send_message":
                await channel.send(params.get("content", "Hello!"))
                result_msg = "Message sent."

            elif action == "mc_broadcast":
                msg = params.get("message", "Announcement from Discord")
                await mc_client.run_command(f"say {msg}")
                result_msg = "Broadcasted message to Minecraft server."

            elif action == "review_whitelist":
                # Import here to avoid circular import if any
                from mcp_server.server import get_whitelist_applications
                apps = await get_whitelist_applications()
                if not apps or "error" in str(apps):
                    result_msg = "No pending whitelist applications found bro."
                else:
                    count = len(apps)
                    result_msg = f"Found {count} pending whitelist applications. You can check them on the official dashboard."

            else:
                result_msg = f"Action {action} is not fully implemented yet."

            # 4. Humanize Result
            return humanizer.humanize(result_msg)

        except Exception as e:
            core_logger.error(f"Action execution failed: {e}")
            return "onnu hang aayi bro, action cheyyan pattilla 😭"

action_executor = ActionExecutor()
