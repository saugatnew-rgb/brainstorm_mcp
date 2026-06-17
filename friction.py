"""
friction.py — Surrender signal detection and friction injection.
The core logic that prevents premature closure in brainstorming.
"""

import random
from typing import Optional

# ── Surrender signals ────────────────────────────────────────────────────────

SURRENDER_PHRASES = [
    "that makes sense", "yes exactly", "good idea", "i agree", "great point",
    "that's right", "perfect", "that works", "sounds good", "absolutely",
    "you're right", "makes sense", "i think so too", "yeah", "yes",
    "ok", "okay", "sure", "indeed", "exactly", "correct", "true",
    "that's a good point", "i hadn't thought of that", "nice", "brilliant",
]

SHORT_RESPONSE_THRESHOLD = 15  # words — short replies after AI suggestion = surrender signal


def detect_surrender(human_message: str, after_ai_suggestion: bool = True) -> bool:
    """
    Returns True if the human appears to be surrendering to the AI's idea
    without genuine critical engagement.
    """
    message_lower = human_message.lower().strip()
    word_count = len(message_lower.split())

    # Short response after AI suggestion
    if after_ai_suggestion and word_count < SHORT_RESPONSE_THRESHOLD:
        return True

    # Explicit surrender phrases
    for phrase in SURRENDER_PHRASES:
        if phrase in message_lower:
            return True

    return False


# ── Friction techniques ───────────────────────────────────────────────────────

CHALLENGE_QUESTIONS = [
    "What evidence would completely disprove this idea?",
    "Who would be most harmed by this, and why might they be right to resist it?",
    "What assumption are we making here that we haven't questioned yet?",
    "If this idea failed spectacularly in five years, what would be the reason?",
    "What does someone from a completely different culture or background think about this?",
    "What are we NOT seeing because we're too close to this problem?",
    "What would a sceptical expert say is the fatal flaw here?",
    "If resources were unlimited, would this still be the best idea?",
    "What is the simplest version of this that still works — and why aren't we doing that?",
    "What would change your mind about this completely?",
]

OPPOSITE_PROMPTS = [
    "Here is the exact opposite argument — and it might be just as valid: ",
    "A strong countercase: ",
    "What if everything we've assumed is backwards? Consider this: ",
    "Devil's advocate — the strongest case against this idea: ",
    "Reverse the premise entirely: ",
]

SELF_ARGUE_PROMPTS = [
    "Now argue the opposite of what you just said. What is the strongest case against your own position?",
    "Steelman the counterargument. If you had to defend the opposite view, what would you say?",
    "Pretend you are someone who completely disagrees with you. What are their three best points?",
    "What would you say if your job was to convince others this idea is wrong?",
    "List three reasons why someone smarter than you might reject this idea.",
]

FRICTION_TYPES = ["challenge_question", "opposite_view", "self_argue"]


def inject_friction(ai_suggestion: str) -> dict:
    """
    Randomly selects a friction technique and returns the friction payload.
    Returns a dict with 'type' and 'friction_text'.
    """
    friction_type = random.choice(FRICTION_TYPES)

    if friction_type == "challenge_question":
        question = random.choice(CHALLENGE_QUESTIONS)
        return {
            "type": "challenge_question",
            "friction_text": f"⚡ Hold on — before you accept that:\n\n**{question}**\n\nTake a moment. What is your honest answer?",
        }

    elif friction_type == "opposite_view":
        prompt = random.choice(OPPOSITE_PROMPTS)
        return {
            "type": "opposite_view",
            "friction_text": (
                f"⚡ {prompt}\n\n"
                f"*[The opposite of the AI suggestion would be explored here — "
                f"push back on: \"{ai_suggestion[:120]}...\"]*\n\n"
                f"Does this opposite view reveal anything the original idea missed?"
            ),
        }

    else:  # self_argue
        prompt = random.choice(SELF_ARGUE_PROMPTS)
        return {
            "type": "self_argue",
            "friction_text": f"⚡ Not so fast.\n\n**{prompt}**",
        }


def build_friction_response(human_message: str, ai_suggestion: str) -> Optional[str]:
    """
    Master function: checks for surrender, injects friction if detected.
    Returns friction text if surrender detected, None otherwise.
    """
    if detect_surrender(human_message, after_ai_suggestion=True):
        payload = inject_friction(ai_suggestion)
        return payload["friction_text"]
    return None
