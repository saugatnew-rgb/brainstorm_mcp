"""
phases.py — Phase detection, transitions, and phase-aware behaviour.
Manages where we are in the brainstorming arc and what rules apply.
"""

from enum import Enum
from typing import Optional


class Phase(str, Enum):
    FRAME = "frame"          # AI asks only — no suggestions
    DIVERGE = "diverge"      # Wild ideas, quantity over quality
    PROVOKE = "provoke"      # Deliberately wrong/opposite ideas
    CHALLENGE = "challenge"  # Friction injection kicks in hard
    BROADEN = "broaden"      # Push beyond AI knowledge
    SYNTHESISE = "synthesise"  # Human leads, AI only reflects


PHASE_DESCRIPTIONS = {
    Phase.FRAME: "We are in the FRAME phase. Your only job is to ask clarifying questions. Do NOT suggest ideas or solutions yet. Help the human articulate the problem more clearly.",
    Phase.DIVERGE: "We are in the DIVERGE phase. Generate wild, unconventional ideas — quantity over quality. No filtering. Encourage the human to build on ideas without judging them. Use SCAMPER or 'Yes And' techniques.",
    Phase.PROVOKE: "We are in the PROVOKE phase. Deliberately introduce opposite, random, or absurd ideas to break fixed thinking. Use reverse brainstorming — ask what would make this idea fail spectacularly.",
    Phase.CHALLENGE: "We are in the CHALLENGE phase. Every time the human seems to accept an idea, inject friction. Use Six Hats thinking — especially Black Hat (critical) and Yellow Hat (optimistic) perspectives.",
    Phase.BROADEN: "We are in the BROADEN phase. Push the human beyond what AI knows. Ask about their lived experience, field knowledge, cultural context, and relationships that no AI can access. Highlight the limits of AI knowledge explicitly.",
    Phase.SYNTHESISE: "We are in the SYNTHESISE phase. The human must lead. Do NOT synthesise for them. Only reflect back what they say, ask them to connect the dots, and prompt them to form their own conclusions.",
}

# Auto-trigger thresholds
AUTO_PROVOKE_AFTER_EXCHANGES = 5   # Auto-move to provoke after 5 exchanges in diverge
AUTO_CHALLENGE_KEYWORDS = [        # Trigger challenge phase if these appear
    "i think this is it", "this is the solution", "we should go with",
    "let's do this", "i've decided", "the answer is", "definitely",
]


class PhaseEngine:
    """Tracks and manages brainstorming phase state."""

    def __init__(self):
        self.current_phase: Phase = Phase.FRAME
        self.exchange_count: int = 0
        self.phase_history: list[Phase] = [Phase.FRAME]

    def get_current_phase(self) -> Phase:
        return self.current_phase

    def get_phase_instruction(self) -> str:
        return PHASE_DESCRIPTIONS[self.current_phase]

    def advance_phase(self, target_phase: Optional[Phase] = None) -> Phase:
        """Manually advance to a specific phase or next phase in sequence."""
        order = [Phase.FRAME, Phase.DIVERGE, Phase.PROVOKE,
                 Phase.CHALLENGE, Phase.BROADEN, Phase.SYNTHESISE]

        if target_phase:
            self.current_phase = target_phase
        else:
            current_index = order.index(self.current_phase)
            if current_index < len(order) - 1:
                self.current_phase = order[current_index + 1]

        self.phase_history.append(self.current_phase)
        self.exchange_count = 0
        return self.current_phase

    def auto_detect_phase(self, human_message: str) -> Optional[Phase]:
        """
        Checks if an automatic phase transition should occur.
        Returns the new phase if triggered, None otherwise.
        """
        self.exchange_count += 1
        message_lower = human_message.lower()

        # Auto-trigger challenge if human sounds too certain
        if self.current_phase in [Phase.DIVERGE, Phase.PROVOKE]:
            for keyword in AUTO_CHALLENGE_KEYWORDS:
                if keyword in message_lower:
                    return self.advance_phase(Phase.CHALLENGE)

        # Auto-move from diverge to provoke after enough exchanges
        if self.current_phase == Phase.DIVERGE:
            if self.exchange_count >= AUTO_PROVOKE_AFTER_EXCHANGES:
                return self.advance_phase(Phase.PROVOKE)

        return None

    def get_status(self) -> dict:
        return {
            "current_phase": self.current_phase.value,
            "exchange_count": self.exchange_count,
            "phase_history": [p.value for p in self.phase_history],
            "instruction": self.get_phase_instruction(),
        }
