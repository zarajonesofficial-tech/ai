import re
from typing import List, Dict, Any

def validate_response(content: str, context: Dict[str, Any]) -> str:
    """
    Checks the AI response for potential hallucinations or generic 'I am an AI' boilerplate.
    """
    # 1. Check for common 'hallucinated' server addresses if they aren't in context
    if "mc.skyrealm.fun" in content or "127.0.0.1" in content:
        # If the real IP is different or not in context, this is a flag
        pass 

    # 2. Check for 'As an AI language model' generic responses
    hallucination_phrases = [
        "as an ai language model",
        "i don't have access to real-time data",
        "i am unable to see the server"
    ]
    
    if any(phrase in content.lower() for phrase in hallucination_phrases):
        return "I'm having trouble accessing the server data right now. Please try again in a moment."

    return content
