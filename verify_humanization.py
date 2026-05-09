import asyncio
from ai.orchestrator.humanizer import humanizer
from ai.orchestrator.main import orchestrator
from ai.orchestrator.social_memory import social_memory
from utils.logger import setup_logging

# Setup logging
setup_logging(debug=True)

async def verify_humanization():
    print("\n" + "="*60)
    print("VERIFYING RESPONSE HUMANIZATION LAYER")
    print("="*60)

    # TEST 1: Direct Humanizer Test
    print("\n[TEST 1] Testing Jargon Stripping...")
    bad_text = "According to the REAL-TIME SYSTEM CONTEXT, Minecraft Server Data shows connection refused."
    good_text = humanizer.humanize(bad_text)
    print(f"INPUT: {bad_text}")
    print(f"OUTPUT: {good_text}")

    # TEST 2: Orchestrator Social Mode Integration
    print("\n[TEST 2] Testing Orchestrator Integration (Social Mode)...")
    channel_id = 777
    user_msg = "server eppo varum? maintenance aano?"
    # Note: We expect the AI to NOT use the bad words because of the new prompt,
    # but the humanizer is there as a safety net.
    response = await orchestrator.handle_query(user_msg, channel_id=channel_id)
    print(f"USER: {user_msg}")
    print(f"AI: {response}")

    print("\n" + "="*60)
    print("HUMANIZATION VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(verify_humanization())
