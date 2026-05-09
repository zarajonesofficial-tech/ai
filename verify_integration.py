import asyncio
import httpx
from core.config import settings
from ai.orchestrator.main import orchestrator
from utils.logger import setup_logging

# Setup logging
setup_logging(debug=True)

async def test_whitelist_integration():
    print("\n" + "="*60)
    print("VERIFYING CROSS-BOT WHITELIST INTEGRATION")
    print("="*60)

    # 1. Direct API Test
    print(f"\n[TEST 1] Testing Direct API connection to {settings.OFFICIAL_BOT_API}...")
    url = f"{settings.OFFICIAL_BOT_API}/api/whitelist/applications"
    headers = {"X-AI-PLATFORM-KEY": settings.INTERNAL_API_KEY}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10.0)
            print(f"STATUS CODE: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS: Retrieved {len(data)} applications.")
                if data:
                    print(f"PREVIEW: {str(data[0])[:100]}...")
            elif response.status_code == 401:
                print("❌ FAILED: Unauthorized. Secret key might not match on VPS.")
            else:
                print(f"❌ FAILED: Received error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: Could not connect: {e}")

    # 2. AI Orchestrator Test
    print("\n[TEST 2] Testing AI Orchestrator Review Intent...")
    query = "bro, check the whitelist for me. any new apps?"
    # Process through master orchestrator (passing mock channel for social mode)
    class MockChannel: 
        def __init__(self): self.id = 111
    
    response = await orchestrator.handle_query(query, channel=MockChannel())
    print(f"USER: {query}")
    print(f"AI: {response}")

    print("\n" + "="*60)
    print("INTEGRATION VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_whitelist_integration())
