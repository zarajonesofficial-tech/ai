import asyncio
import json
from ai.orchestrator.main import orchestrator
from ai.orchestrator.social_memory import social_memory
from utils.logger import setup_logging

# Setup logging
setup_logging(debug=True)

async def verify_social_intelligence():
    print("\n" + "="*70)
    print("VERIFYING ADVANCED SOCIAL CONTEXT INTELLIGENCE")
    print("="*70)

    # Mock 1: Admin in Staff Chat
    print("\n[TEST 1] Admin in Staff Chat (Expect Operational Tone)...")
    context_admin = {
        "author": {"display_name": "CHRIZ", "permissions": {"admin": True, "moderator": True}},
        "channel": {"name": "staff-chat", "type": "text"},
        "reply_context": {}
    }
    q1 = "give me a server health update"
    resp1 = await orchestrator.handle_query(q1, social_context=context_admin)
    print(f"USER (Admin): {q1}")
    print(f"AI RESPONSE: {resp1}")

    # Mock 2: Member in General Chat
    print("\n[TEST 2] Member in General Chat (Expect Casual Manglish)...")
    context_member = {
        "author": {"display_name": "RandomPlayer", "permissions": {"admin": False, "moderator": False}},
        "channel": {"name": "general-chat", "type": "text"},
        "reply_context": {}
    }
    q2 = "entha bro vishesham? server lag ano?"
    resp2 = await orchestrator.handle_query(q2, social_context=context_member)
    print(f"USER (Member): {q2}")
    print(f"AI RESPONSE: {resp2}")

    # Mock 3: Reply awareness
    print("\n[TEST 3] Reply Chain Awareness...")
    context_reply = {
        "author": {"display_name": "RandomPlayer", "permissions": {"admin": False, "moderator": False}},
        "channel": {"name": "general-chat", "type": "text"},
        "reply_context": {
            "reply_to_user": "CHRIZ__3656 AI",
            "reply_to_message": "onnu hang aayi bro, pinne nokkam 😭"
        }
    }
    q3 = "yeyyy you are back! are you working now?"
    resp3 = await orchestrator.handle_query(q3, social_context=context_reply)
    print(f"USER (Reply): {q3}")
    print(f"AI RESPONSE: {resp3}")

    print("\n" + "="*70)
    print("SOCIAL INTELLIGENCE VERIFICATION COMPLETE")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(verify_social_intelligence())
