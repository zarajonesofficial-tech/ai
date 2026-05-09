import re
from typing import Dict

class ResponseHumanizer:
    """
    Ensures AI responses sound like a human community member and not an orchestration engine.
    Strips internal technical jargon and translates operational data into casual language.
    """
    
    # Internal terms to strip or replace
    LEAKY_PHRASES: Dict[str, str] = {
        r"according to the REAL-TIME SYSTEM CONTEXT": "njan check cheythappol",
        r"REAL-TIME SYSTEM CONTEXT": "server details",
        r"Minecraft Server Data": "server side",
        r"retrieved context": "details",
        r"operational state": "status",
        r"connection refused": "connect aavunilla bro 😭",
        r"multiple exceptions": "kurach scene und",
        r"internal error": "onnu hang aayi",
        r"provided context": "njan nokkiya details",
        r"as an AI assistant": "",
        r"as an AI language model": "",
        r"infrastructure AI": "community member",
    }

    def humanize(self, text: str) -> str:
        """
        Runs a naturalization pass over the generated text.
        """
        # 1. Strip common AI boilerplate
        text = text.replace("I am just an AI assistant.", "")
        text = text.replace("How can I help you today?", "")
        
        # 2. Replace technical leaks with casual Manglish/English
        for pattern, replacement in self.LEAKY_PHRASES.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # 3. Clean up whitespace and punctuation
        text = text.strip().strip(".").strip()
        
        # 4. Final 'Human' Nudge: If it's too long, trim it (social chats should be punchy)
        if len(text.split()) > 50:
            # We don't want to cut off useful info, but we encourage the LLM 
            # to be short via the prompt. This is just a safety.
            pass
            
        return text

humanizer = ResponseHumanizer()
