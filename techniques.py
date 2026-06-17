"""
techniques.py — Established brainstorming technique library.
Maps techniques to phases and provides prompts for each.
"""

from enum import Enum
from typing import Optional
import random


class Technique(str, Enum):
    SCAMPER = "scamper"
    SIX_HATS = "six_hats"
    REVERSE = "reverse_brainstorming"
    RANDOM_WORD = "random_word"
    ANALOGICAL = "analogical_thinking"
    YES_AND = "yes_and"


TECHNIQUE_PHASE_MAP = {
    "diverge": [Technique.SCAMPER, Technique.YES_AND, Technique.RANDOM_WORD],
    "provoke": [Technique.REVERSE, Technique.RANDOM_WORD],
    "challenge": [Technique.SIX_HATS, Technique.REVERSE],
    "broaden": [Technique.ANALOGICAL, Technique.SIX_HATS],
}

SCAMPER_PROMPTS = [
    "**Substitute**: What if you replaced the core element of this idea with something completely different?",
    "**Combine**: What two unrelated ideas could you merge to create something new?",
    "**Adapt**: What exists in nature or another industry that solves this same problem?",
    "**Modify/Magnify**: What happens if you make this 10x bigger, faster, or more extreme?",
    "**Put to other uses**: How could this idea solve a completely different problem?",
    "**Eliminate**: What is the absolute minimum version — what can you remove entirely?",
    "**Reverse/Rearrange**: What if the order was flipped — the end becomes the beginning?",
]

SIX_HATS_PROMPTS = {
    "white": "🎩 White Hat — Facts only: What do we actually *know* for certain about this? What data do we have?",
    "black": "🎩 Black Hat — Critical: What are the risks, dangers, and reasons this could fail?",
    "yellow": "🎩 Yellow Hat — Optimistic: What is the best possible outcome? What value does this create?",
    "green": "🎩 Green Hat — Creative: What wild alternatives haven't we considered yet?",
    "red": "🎩 Red Hat — Emotional: What does your gut say? What feeling does this give you?",
    "blue": "🎩 Blue Hat — Process: Are we asking the right question? Are we stuck in a rut?",
}

REVERSE_PROMPTS = [
    "Reverse brainstorm: How would you make this idea fail as badly as possible?",
    "What would you do if your goal was the opposite — to make things worse?",
    "List everything that could go wrong. Now flip each one — what does that reveal about what *should* go right?",
    "If you wanted to guarantee nobody used this — what would you design?",
]

RANDOM_WORDS = [
    "cloud", "bridge", "mirror", "river", "anchor", "seed", "telescope",
    "ladder", "compass", "flame", "thread", "echo", "lighthouse", "current",
]

ANALOGICAL_PROMPTS = [
    "How does nature solve this same problem? Think of animals, ecosystems, weather patterns.",
    "What industry completely unrelated to yours has already solved this? What can you borrow?",
    "If this problem were a physical object, what would it look like — and how would you fix it?",
    "Think of a children's story that has a similar challenge. How did it resolve?",
    "What would a chef, an architect, and a doctor each say about this problem?",
]

YES_AND_PROMPTS = [
    "Yes, and... take the last idea and add one more element to make it bigger or stranger.",
    "Accept the previous idea completely, then build one unexpected layer on top of it.",
    "Don't evaluate — just extend. Say 'yes and' to whatever came before.",
]


def get_technique_prompt(technique: Technique, topic: str = "") -> str:
    """Returns a prompt for the given technique."""

    if technique == Technique.SCAMPER:
        prompt = random.choice(SCAMPER_PROMPTS)
        return f"**SCAMPER Technique**\n\n{prompt}\n\nApply this to: *{topic}*"

    elif technique == Technique.SIX_HATS:
        hat = random.choice(list(SIX_HATS_PROMPTS.keys()))
        prompt = SIX_HATS_PROMPTS[hat]
        return f"**Six Thinking Hats**\n\n{prompt}\n\nContext: *{topic}*"

    elif technique == Technique.REVERSE:
        prompt = random.choice(REVERSE_PROMPTS)
        return f"**Reverse Brainstorming**\n\n{prompt}\n\nTopic: *{topic}*"

    elif technique == Technique.RANDOM_WORD:
        word = random.choice(RANDOM_WORDS)
        return (
            f"**Random Word Stimulus**\n\n"
            f"Random word: **{word}**\n\n"
            f"Force a connection: How does '{word}' relate to *{topic}*? "
            f"Don't think — just say the first connection that comes to mind."
        )

    elif technique == Technique.ANALOGICAL:
        prompt = random.choice(ANALOGICAL_PROMPTS)
        return f"**Analogical Thinking**\n\n{prompt}\n\nProblem: *{topic}*"

    elif technique == Technique.YES_AND:
        prompt = random.choice(YES_AND_PROMPTS)
        return f"**Yes And**\n\n{prompt}"

    return f"Apply creative thinking to: {topic}"


def get_technique_for_phase(phase_name: str, topic: str = "") -> Optional[str]:
    """Returns a technique prompt appropriate for the current phase."""
    techniques = TECHNIQUE_PHASE_MAP.get(phase_name, [])
    if not techniques:
        return None
    technique = random.choice(techniques)
    return get_technique_prompt(technique, topic)
