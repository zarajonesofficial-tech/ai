import asyncio
from ai.orchestrator.main import orchestrator
from ai.orchestrator.master_intent_router import Intent, intent_router
from utils.logger import setup_logging

# Setup logging
setup_logging(debug=True)

async def verify_orchestration_stablity():
    print("\n" + "="*60)
    print("VERIFYING MASTER INTENT ROUTING & STABILITY")
    print("="*60)

    # TEST 1: Workflow Detection
    print("\n[TEST 1] Testing Workflow Detection...")
    q1 = "announce maintenance and then restart the server"
    intent1 = await intent_router.route(q1)
    print(f"QUERY: '{q1}'")
    print(f"INTENT: {intent1.value}")
    if intent1 == Intent.WORKFLOW:
        print("✅ PASSED")
    else:
        print("❌ FAILED")

    # TEST 2: Action Detection (Security Alert)
    print("\n[TEST 2] Testing Action Detection...")
    q2 = "mention everyone right now"
    intent2 = await intent_router.route(q2)
    print(f"QUERY: '{q2}'")
    print(f"INTENT: {intent2.value}")
    if intent2 == Intent.ACTION:
        print("✅ PASSED")
    else:
        print("❌ FAILED")

    # TEST 3: Factual vs Social Confusion Fix
    print("\n[TEST 3] Testing Factual vs Social Clarity...")
    q3 = "what is the server status?"
    intent3 = await intent_router.route(q3)
    print(f"QUERY: '{q3}'")
    print(f"INTENT: {intent3.value}")
    if intent3 == Intent.FACTUAL:
        print("✅ PASSED")
    else:
        print("❌ FAILED")

    # TEST 4: Humanization Safety (Anti-Leak)
    print("\n[TEST 4] Testing Anti-Leak Verification...")
    # Mock a social query with a proper mock object
    class MockChannel:
        def __init__(self): self.id = 999
    
    q4 = "bro status entha?"
    response = await orchestrator.handle_query(q4, channel=MockChannel())
    print(f"QUERY: '{q4}'")
    print(f"RESPONSE: {response}")
    
    leaks = ["REAL-TIME SYSTEM CONTEXT", "Minecraft Server Data", "retrieved context"]
    if any(leak in response for leak in leaks):
        print("❌ FAILED: Technical terminology leaked!")
    else:
        print("✅ PASSED: No technical leakage found.")

    print("\n" + "="*60)
    print("STABILIZATION VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(verify_orchestration_stablity())
