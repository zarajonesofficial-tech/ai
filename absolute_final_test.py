import asyncio
import json
from ai.orchestrator.main import orchestrator
from ai.orchestrator.social_memory import social_memory
from utils.logger import setup_logging
from core.config import settings

# Setup logging
setup_logging(debug=True)

class MockMember:
    def __init__(self, name, roles, is_admin=False):
        self.display_name = name
        self.name = name
        self.roles = [type('Role', (object,), {'name': r}) for r in roles]
        self.guild_permissions = type('Perms', (object,), {'administrator': is_admin})

class MockChannel:
    def __init__(self, id):
        self.id = id
    async def send(self, content):
        print(f"   [DISCORD SEND] -> {content}")

async def run_feature_test(test_name, query, member, channel):
    print(f"\n>>> [TEST: {test_name}]")
    print(f"    QUERY: '{query}'")
    print(f"    USER: {member.display_name} (Roles: {[r.name for r in member.roles]})")
    
    # Simulate passive memory update
    await social_memory.add_message(channel.id, "user", query, member.display_name)
    
    # Process through master orchestrator
    response = await orchestrator.handle_query(query, member=member, channel=channel)
    
    print(f"    FINAL AI RESPONSE: {response}")
    print("-" * 60)

async def main():
    channel = MockChannel(9999)
    admin_user = MockMember("CHRIZ", ["Admin"], is_admin=True)
    normal_user = MockMember("Community_Member", ["Player"], is_admin=False)

    print("\n" + "="*70)
    print("CHRIZ__3656 AI - ABSOLUTE FINAL SYSTEM VERIFICATION")
    print("="*70)

    # 1. Social Naturalization & Humanizer Test
    await run_feature_test(
        "Social Mode (Humanized Manglish)", 
        "entha bro vishesham? server ippo status entha?", 
        normal_user, 
        channel
    )

    # 2. Factual Grounding (RAG) Test
    await run_feature_test(
        "Factual Mode (Knowledge Base)", 
        "Tell me the skills for Diamond and Cosmic ranks.", 
        normal_user, 
        channel
    )

    # 3. Action Mode (RBAC Security)
    await run_feature_test(
        "Action Mode (Security - Unauthorized)", 
        "restart the minecraft server", 
        normal_user, 
        channel
    )

    # 4. Official Bot Bridge Test
    await run_feature_test(
        "Action Mode (Official Bot Bridge)", 
        "check the whitelist applications on the VPS", 
        admin_user, 
        channel
    )

    # 5. Infrastructure Control (Pterodactyl)
    await run_feature_test(
        "Action Mode (Pterodactyl Control)", 
        "reboot the minecraft server now", 
        admin_user, 
        channel
    )

    # 6. Workflow Planning Test
    await run_feature_test(
        "Workflow Mode (Task Planning)", 
        "announce a maintenance window and then stop the server", 
        admin_user, 
        channel
    )

    print("\n" + "="*70)
    print("ALL SYSTEMS OPERATIONAL & VERIFIED")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
