import re
from typing import Dict

class ResponseHumanizer:
    """
    Advanced Response Humanization Layer.
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
        r"operational injection": "live updates",
        r"Minecraft server connection": "server connection",
        r"connection is currently refused": "connect aavunilla bro 😭",
        r"error": "scene",
        r"indicated": "parayunne",
        r"indicates": "parayunne",
        r"suggests": "thonunnu",
        r"explicitly": "",
        r"information about": "details",
        r"current status": "ippathe scene",
        r"multiple exceptions": "kurach scene und",
        r"internal error": "onnu hang aayi",
        r"provided context": "njan nokkiya details",
        r"as an AI assistant": "",
        r"as an AI language model": "",
        r"infrastructure AI": "community member",
        r"orchestration terminology": "",
        r"system pipeline": "back-end",
        r"debug language": "logs",
        r"retrieval terminology": "details",
    }

    def humanize(self, text: str) -> str:
        """
        Runs a naturalization pass over the generated text.
        """
        # 1. Strip common AI boilerplate and formal assistant speech
        boilerplate = [
            "I am just an AI assistant.",
            "How can I help you today?",
            "As an AI, I don't have feelings.",
            "I am an artificial intelligence designed by Chriz.",
            "I'm sorry, but I don't have access to your personal life."
        ]
        for phrase in boilerplate:
            text = text.replace(phrase, "")
        
        # 2. Replace technical leaks with casual Manglish/English
        for pattern, replacement in self.LEAKY_PHRASES.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # 3. Clean up whitespace and punctuation
        text = text.strip().strip(".").strip()
        
        return text

humanizer = ResponseHumanizer()
