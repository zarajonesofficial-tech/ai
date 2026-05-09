import asyncio
import json
from ai.orchestrator.main import orchestrator
from ai.orchestrator.master_intent_router import intent_router
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
    channel = MockChannel(8888)
    admin_user = MockMember("Chriz", ["Admin"], is_admin=True)
    normal_user = MockMember("Player_One", ["Member"], is_admin=False)

    print("\n" + "="*70)
    print("CHRIZ__3656 AI - FULL SYSTEM FINAL VERIFICATION")
    print("="*70)

    # 1. Social Test (Manglish + Casual)
    await run_feature_test(
        "Social/Manglish", 
        "entha bro vishesham? bot set aano?", 
        normal_user, 
        channel
    )

    # 2. Factual Test (Knowledge Base)
    await run_feature_test(
        "Factual/KB", 
        "What are the skills for Astral rank?", 
        normal_user, 
        channel
    )

    # 3. Action Test (Security Check - Should Deny)
    await run_feature_test(
        "Action/Security (Unauthorized)", 
        "mention everyone", 
        normal_user, 
        channel
    )

    # 4. Action Test (Authorized)
    await run_feature_test(
        "Action/Authorized", 
        "mention everyone", 
        admin_user, 
        channel
    )

    # 5. Workflow Test (Task Planning)
    await run_feature_test(
        "Workflow/Planning", 
        "announce maintenance and then restart the server", 
        admin_user, 
        channel
    )

    # 6. Memory Test
    await run_feature_test(
        "Conversational Memory", 
        "who was I talking about in my first message?", 
        normal_user, 
        channel
    )

    print("\n" + "="*70)
    print("FINAL VERIFICATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
