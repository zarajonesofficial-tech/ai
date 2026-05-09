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
        r"according to the provided context": "njan check cheythappol",
        r"based on the provided context": "njan check cheythappol",
        r"according to the REAL-TIME SYSTEM CONTEXT": "njan check cheythappol",
        r"based on the REAL-TIME SYSTEM CONTEXT": "njan check cheythappol",
        r"the current status indicates": "looks like",
        r"current status indicates": "looks like",
        r"the current status suggests": "looks like",
        r"according to the REAL-TIME SYSTEM CONTEXT": "njan check cheythappol",
        r"REAL-TIME SYSTEM CONTEXT": "server details",
        r"Minecraft Server Data": "server side",
        r"retrieved context": "details",
        r"operational state": "status",
        r"operational injection": "live updates",
        r"Minecraft server connection": "server connection",
        r"connection is currently refused": "connect aavunilla bro 😭",
        r"\bindicated\b": "showed",
        r"\bindicates\b": "shows",
        r"\bsuggests\b": "looks like",
        r"explicitly": "",
        r"information about": "details about",
        r"current status": "status",
        r"multiple exceptions": "kurach scene und",
        r"internal error": "onnu hang aayi",
        r"provided context": "details",
        r"as an AI assistant": "",
        r"as an AI language model": "",
        r"infrastructure AI": "community member",
        r"orchestration terminology": "",
        r"system pipeline": "back-end",
        r"debug language": "logs",
        r"retrieval terminology": "details",
    }

    OPENING_CLEANUPS = [
        r"^(sure|yeah|yep|alright|okay)[,!\s]+",
        r"^(as per|based on|from) (the )?(details|info)[,:\s]+",
        r"^according to\s+",
    ]

    REPETITIVE_FILLERS = [
        "bro bro",
        "macha macha",
        "scene scene",
        "okay bro bro",
    ]

    def _normalize_opening(self, text: str) -> str:
        for pattern in self.OPENING_CLEANUPS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text

    def _reduce_repetition(self, text: str) -> str:
        for phrase in self.REPETITIVE_FILLERS:
            base = phrase.split()[0]
            text = re.sub(re.escape(phrase), base, text, flags=re.IGNORECASE)

        # Collapse duplicate punctuation and overdone emoji runs.
        text = re.sub(r"([!?.,])\1{1,}", r"\1", text)
        text = re.sub(r"(👀|😭|🔥|✨)\s*(\1\s*){1,}", r"\1 ", text)
        text = re.sub(r"\b(bro|macha|scene)\b(?:\s+\1\b)+", r"\1", text, flags=re.IGNORECASE)
        return text

    def _soften_formality(self, text: str) -> str:
        replacements = {
            r"\bI do not have that information\b": "I don't have that info rn",
            r"\bI do not have access to\b": "I can't check",
            r"\bI cannot confirm\b": "I can't confirm",
            r"\bI am unable to\b": "I can't",
            r"\bplease note that\b": "",
            r"\bit appears that\b": "looks like",
            r"\bright now\b": "rn",
        }
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

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

        # 3. Reduce robotic structure and repetitive slang.
        text = self._normalize_opening(text)
        text = self._soften_formality(text)
        text = self._reduce_repetition(text)

        # 4. Clean up whitespace and punctuation
        text = re.sub(r"\s+", " ", text).strip()
        text = text.strip(".").strip()
        
        return text

humanizer = ResponseHumanizer()
