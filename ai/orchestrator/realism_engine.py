import random
from typing import List, Dict, Any

class RealismEngine:
    """
    Manages conversational realism, variation, and pacing.
    Prevents repetitive phrasing and ensures natural, non-robotic responses.
    """
    
    VARIATION_RULES = [
        "Vary your sentence lengths. Some should be very short, others more descriptive.",
        "Do not use the same greeting or filler word (like 'bro') in every message.",
        "Occasionally drop all emojis to sound more serious or relaxed.",
        "Use natural Manglish code-switching only when it feels authentic to the conversation.",
        "If you just used a specific slang word, avoid using it again for a few turns."
    ]

    def get_realism_instructions(self) -> str:
        """Returns a random subset of realism rules to ensure variation over time."""
        # Selection of 2-3 rules per turn ensures the AI behavior isn't static
        selected = random.sample(self.VARIATION_RULES, k=3)
        
        return "\n### 🎭 CONVERSATIONAL REALISM RULES:\n- " + "\n- ".join(selected)

    def apply_pacing(self, content: str) -> str:
        """
        Final post-processing to adjust pacing. 
        Example: Randomly deciding to remove trailing emojis if they feel forced.
        """
        # (Optional: implement logic to detect and reduce emoji spam if LLM fails)
        return content.strip()

realism_engine = RealismEngine()
