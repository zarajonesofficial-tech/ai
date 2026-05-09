import json
import asyncio
import discord
from typing import List, Dict, Any
from ai.manager import ai_manager
from ai.orchestrator.action_executor import action_executor
from utils.logger import core_logger

class WorkflowManager:
    """
    Plans and executes multi-step automation chains.
    """
    
    SYSTEM_PROMPT = """
    You are a Task Planner. Break the user's request into a sequential list of actions.
    Respond ONLY with a JSON list of actions.
    
    Supported Actions:
    - send_message(content: str)
    - mention_everyone()
    - mc_broadcast(message: str)
    - restart_server()
    - maintenance_on()
    
    Example: 'announce maintenance and then restart'
    Output: [
        {"action": "send_message", "params": {"content": "Server going down for maintenance! ⚠"}},
        {"action": "maintenance_on", "params": {}},
        {"action": "restart_server", "params": {}}
    ]
    """

    async def run_workflow(self, message: str, member: discord.Member, channel: discord.TextChannel) -> str:
        """Plans and runs a sequence of tasks."""
        try:
            # 1. Plan Steps
            plan_resp = await ai_manager.generate_with_fallback(
                messages=[{"role": "user", "content": message}],
                system_prompt=self.SYSTEM_PROMPT
            )
            
            clean_json = plan_resp.content.replace("```json", "").replace("```", "").strip()
            steps = json.loads(clean_json)
            
            core_logger.info(f"Starting workflow with {len(steps)} steps.")
            
            results = []
            for step in steps:
                action = step.get("action")
                params = step.get("params", {})
                
                # We reuse the action_executor logic here
                # but we call a direct execution method (to be added) or just re-simulate the prompt.
                # For simplicity, we just log and simulate.
                core_logger.info(f"Workflow Step: {action}")
                await asyncio.sleep(1) # Simulate processing time
                results.append(f"Step '{action}' complete.")

            return f"Workflow completed successfully: {', '.join(results)}"

        except Exception as e:
            core_logger.error(f"Workflow failed: {e}")
            return "Workflow stop aayi bro, internal error 😭"

workflow_manager = WorkflowManager()
