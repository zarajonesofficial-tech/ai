import asyncio
from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, patch

from ai.orchestrator.main import orchestrator
from ai.orchestrator.master_intent_router import Intent
from ai.orchestrator.social_memory import social_memory
from ai.providers.base import AIResponse


@dataclass
class Case:
    name: str
    query: str
    intent: Intent
    channel_name: str
    expected_terms: list[str]
    forbidden_terms: list[str]
    should_be_brief: bool = True


CASES = [
    Case(
        name="Casual General",
        query="entha bro vishesham, server oke set aano?",
        intent=Intent.SOCIAL,
        channel_name="general-chat",
        expected_terms=["server", "set"],
        forbidden_terms=["REAL-TIME SYSTEM CONTEXT", "provided context", "AI assistant"],
    ),
    Case(
        name="Lag Question",
        query="server lag ano bro? players complaint parayunnu",
        intent=Intent.SOCIAL,
        channel_name="general-chat",
        expected_terms=["lag"],
        forbidden_terms=["operational state", "retrieved context"],
    ),
    Case(
        name="Factual Rank Question",
        query="bro diamond rankile skills onnu para",
        intent=Intent.FACTUAL,
        channel_name="general-chat",
        expected_terms=["diamond", "heal"],
        forbidden_terms=["REAL-TIME SYSTEM CONTEXT", "knowledge base"],
    ),
    Case(
        name="Serious Support Tone",
        query="bro whitelist apply cheythu but reply vannilla, entha cheyyende",
        intent=Intent.SOCIAL,
        channel_name="support-ticket",
        expected_terms=["whitelist", "check"],
        forbidden_terms=["scene scene", "bro bro"],
    ),
    Case(
        name="Owner Availability",
        query="chriz online undo? urgent anu",
        intent=Intent.FACTUAL,
        channel_name="general-chat",
        expected_terms=["owner", "online"],
        forbidden_terms=["provided context", "operational injection"],
    ),
    Case(
        name="Technical Failure Translation",
        query="rcon connect aavunilla, entha issue?",
        intent=Intent.FACTUAL,
        channel_name="staff-chat",
        expected_terms=["connect", "aavunilla"],
        forbidden_terms=["connection is currently refused", "internal terminology"],
    ),
]


def fake_context(intent: Intent, query: str) -> dict[str, Any]:
    context = {
        "timestamp": "2026-05-09T00:00:00Z",
        "operational_state": {
            "status": "online",
            "owner_available": True,
            "active_events": ["Weekend PvP"],
        },
        "minecraft": {},
        "pterodactyl": {},
        "discord": {},
        "knowledge_base": [],
    }

    if intent == Intent.FACTUAL:
        context["minecraft"] = {"raw_list": "There are 4/100 players online: Alex, Steve, Chriz, Nova"}
        context["knowledge_base"] = [
            {"title": "Diamond Rank", "content": "Diamond rank includes Heal, Feed, and kits."},
            {"title": "Whitelist", "content": "Whitelist review usually happens after staff checks the application queue."},
        ]
    return context


def fake_model_response(user_text: str) -> str:
    lower = user_text.lower()
    if "diamond" in lower:
        return "According to the provided context, Diamond rank includes Heal and Feed bro."
    if "whitelist" in lower:
        return "Based on the provided context, whitelist details are pending and you should check with staff."
    if "online undo" in lower or "online undo?" in lower or "urgent anu" in lower:
        return "According to the REAL-TIME SYSTEM CONTEXT, owner is online right now."
    if "rcon" in lower or "connect aavunilla" in lower:
        return "The current status indicates the connection is currently refused."
    if "lag" in lower:
        return "It appears that the server is online, but there may be lag. I am unable to confirm the exact cause."
    return "Sure, according to the provided context, server is set right now."


async def fake_generate_with_fallback(messages, tools=None, system_prompt=None):
    user_text = messages[-1]["content"]
    return AIResponse(
        content=fake_model_response(user_text),
        raw_response={},
        provider="fake",
        model="fake-model",
    )


async def fake_build_context(intent: Intent, query: str) -> dict[str, Any]:
    return fake_context(intent, query)


async def run_case(case: Case) -> tuple[bool, str]:
    channel_id = abs(hash(case.name)) % 100000 + 1
    await social_memory.clear_history(channel_id)
    await social_memory.add_message(channel_id, "user", "hi bot", "Tester")

    social_context = {
        "author": {
            "display_name": "Tester",
            "permissions": {"admin": False, "moderator": False},
        },
        "channel": {"name": case.channel_name, "type": "text"},
        "reply_context": {},
    }

    with patch("ai.orchestrator.main.ai_manager.generate_with_fallback", new=AsyncMock(side_effect=fake_generate_with_fallback)), \
         patch("ai.orchestrator.main.build_context", new=AsyncMock(side_effect=fake_build_context)), \
         patch("ai.orchestrator.main.intent_router.route", new=AsyncMock(return_value=case.intent)):
        response = await orchestrator.handle_query(
            message=case.query,
            channel=type("Channel", (), {"id": channel_id})(),
            social_context=social_context,
        )

    lowered = response.lower()
    passed = True

    for term in case.expected_terms:
        if term.lower() not in lowered:
            passed = False

    for term in case.forbidden_terms:
        if term.lower() in lowered:
            passed = False

    if case.should_be_brief and len(response.split()) > 30:
        passed = False

    return passed, response


async def main():
    print("\n" + "=" * 72)
    print("MANGGLISH RESPONSE VERIFICATION MATRIX")
    print("=" * 72)

    passed_count = 0
    for case in CASES:
        passed, response = await run_case(case)
        status = "PASS" if passed else "FAIL"
        print(f"\n[{status}] {case.name}")
        print(f"Q: {case.query}")
        print(f"A: {response}")
        if passed:
            passed_count += 1

    print("\n" + "-" * 72)
    print(f"Passed {passed_count}/{len(CASES)} cases")
    print("-" * 72)


if __name__ == "__main__":
    asyncio.run(main())
