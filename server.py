"""
server.py — BrainStorm MCP Server
A brainstorming facilitator that forces critical thinking,
prevents premature closure, and injects productive friction.

Install: pip install mcp fastmcp
Run:     python server.py
"""

import json
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from friction import build_friction_response, detect_surrender
from phases import PhaseEngine, Phase
from techniques import get_technique_for_phase, get_technique_prompt, Technique

# ── Server init ───────────────────────────────────────────────────────────────

mcp = FastMCP("brainstorm_mcp")

# In-memory session state (one session per server instance)
# For multi-user deployment, replace with a session store keyed by user ID
_engine = PhaseEngine()
_last_ai_suggestion: str = ""

# ── Input models ──────────────────────────────────────────────────────────────

class StartSessionInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    topic: str = Field(..., description="The topic or problem the human wants to brainstorm", min_length=3, max_length=500)

class ProcessMessageInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    human_message: str = Field(..., description="The human's latest message in the brainstorming session", min_length=1, max_length=2000)
    ai_suggestion: Optional[str] = Field(default="", description="The AI's previous suggestion (used to detect if human is surrendering to it)", max_length=2000)

class AdvancePhaseInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    target_phase: Optional[str] = Field(
        default=None,
        description="Phase to jump to: frame, diverge, provoke, challenge, broaden, synthesise. Leave empty to advance to next phase."
    )

class TechniqueInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    technique: str = Field(..., description="Technique name: scamper, six_hats, reverse_brainstorming, random_word, analogical_thinking, yes_and")
    topic: str = Field(default="", description="The topic or idea to apply the technique to", max_length=500)

# ── Tools ─────────────────────────────────────────────────────────────────────

@mcp.tool(
    name="brainstorm_start",
    annotations={
        "title": "Start a Brainstorming Session",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
async def brainstorm_start(params: StartSessionInput) -> str:
    """
    Starts a new brainstorming session on a given topic.
    Resets the phase engine to FRAME phase and returns the opening facilitation prompt.
    The facilitator will ask questions only — no suggestions — until the problem is clear.

    Args:
        params (StartSessionInput): Contains:
            - topic (str): The brainstorming topic or problem

    Returns:
        str: JSON with session status and the opening facilitator prompt
    """
    global _engine, _last_ai_suggestion
    _engine = PhaseEngine()
    _last_ai_suggestion = ""

    response = {
        "session_started": True,
        "topic": params.topic,
        "phase": _engine.get_current_phase().value,
        "phase_instruction": _engine.get_phase_instruction(),
        "facilitator_prompt": (
            f"We're going to brainstorm: **{params.topic}**\n\n"
            f"Before we generate any ideas, I want to understand the problem more deeply.\n\n"
            f"**Question 1:** In your own words — not what you've read or been told — "
            f"what is the real core of this problem? What makes it hard?\n\n"
            f"*(Take your time. Don't reach for solutions yet.)*"
        ),
        "rules": [
            "AI will ask before suggesting",
            "You must commit to your own idea before AI responds",
            "AI will challenge you when you seem too comfortable",
            "You synthesise — AI only reflects",
        ]
    }
    return json.dumps(response, indent=2)


@mcp.tool(
    name="brainstorm_process",
    annotations={
        "title": "Process a Human Message in Brainstorming",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
async def brainstorm_process(params: ProcessMessageInput) -> str:
    """
    Processes the human's latest message and returns facilitator guidance.
    Detects surrender signals and injects friction if needed.
    Auto-detects phase transitions based on conversation dynamics.

    Args:
        params (ProcessMessageInput): Contains:
            - human_message (str): What the human just said
            - ai_suggestion (str): The AI's previous suggestion (optional)

    Returns:
        str: JSON with friction (if detected), phase status, technique suggestion, and facilitator guidance
    """
    global _engine, _last_ai_suggestion

    ai_suggestion = params.ai_suggestion or _last_ai_suggestion
    human_message = params.human_message

    # Check for auto phase transition
    new_phase = _engine.auto_detect_phase(human_message)
    phase_changed = new_phase is not None

    # Check for surrender
    friction_text = None
    if ai_suggestion and detect_surrender(human_message):
        friction_text = build_friction_response(human_message, ai_suggestion)

    # Get technique for current phase
    current_phase = _engine.get_current_phase()
    technique_prompt = get_technique_for_phase(current_phase.value, topic=human_message[:100])

    # Build synthesise guard
    synthesise_guard = None
    if current_phase == Phase.SYNTHESISE:
        synthesise_guard = (
            "🛑 **Synthesis belongs to you, not the AI.**\n\n"
            "What connections are YOU seeing? What conclusion is emerging for YOU?\n"
            "The AI will only reflect back what you say."
        )

    response = {
        "phase": current_phase.value,
        "phase_changed": phase_changed,
        "phase_instruction": _engine.get_phase_instruction(),
        "surrender_detected": friction_text is not None,
        "friction": friction_text,
        "technique_suggestion": technique_prompt,
        "synthesise_guard": synthesise_guard,
        "exchange_count": _engine.exchange_count,
        "facilitator_note": (
            "Friction injected — challenge the human before proceeding."
            if friction_text else
            "No surrender detected — continue brainstorming naturally."
        ),
    }
    return json.dumps(response, indent=2)


@mcp.tool(
    name="brainstorm_advance_phase",
    annotations={
        "title": "Manually Advance Brainstorming Phase",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
async def brainstorm_advance_phase(params: AdvancePhaseInput) -> str:
    """
    Manually advances the brainstorming session to a specific phase or the next phase.
    Use when the human explicitly requests to move forward, or when the facilitator
    judges the current phase is complete.

    Args:
        params (AdvancePhaseInput): Contains:
            - target_phase (str, optional): Specific phase name to jump to

    Returns:
        str: JSON with new phase details and transition message
    """
    target = None
    if params.target_phase:
        try:
            target = Phase(params.target_phase.lower())
        except ValueError:
            return json.dumps({"error": f"Unknown phase '{params.target_phase}'. Valid: frame, diverge, provoke, challenge, broaden, synthesise"})

    new_phase = _engine.advance_phase(target)

    transition_messages = {
        Phase.DIVERGE: "🌊 Diverge phase — generate freely. No wrong answers. Quantity wins.",
        Phase.PROVOKE: "⚡ Provoke phase — we're about to challenge everything. Expect disruption.",
        Phase.CHALLENGE: "🔥 Challenge phase — nothing gets accepted easily from here.",
        Phase.BROADEN: "🌍 Broaden phase — push beyond what AI knows. Your experience matters most now.",
        Phase.SYNTHESISE: "🧵 Synthesise phase — you lead. Connect the dots yourself.",
    }

    return json.dumps({
        "new_phase": new_phase.value,
        "phase_instruction": _engine.get_phase_instruction(),
        "transition_message": transition_messages.get(new_phase, "Phase advanced."),
        "phase_history": _engine.status()["phase_history"] if hasattr(_engine, "status") else [],
    }, indent=2)


@mcp.tool(
    name="brainstorm_technique",
    annotations={
        "title": "Apply a Brainstorming Technique",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
async def brainstorm_technique(params: TechniqueInput) -> str:
    """
    Returns a structured prompt for a specific brainstorming technique.
    Techniques: SCAMPER, Six Hats, Reverse Brainstorming, Random Word, Analogical Thinking, Yes And.

    Args:
        params (TechniqueInput): Contains:
            - technique (str): Technique name
            - topic (str): Topic to apply the technique to

    Returns:
        str: JSON with the technique prompt ready to present to the human
    """
    technique_map = {
        "scamper": Technique.SCAMPER,
        "six_hats": Technique.SIX_HATS,
        "reverse_brainstorming": Technique.REVERSE,
        "random_word": Technique.RANDOM_WORD,
        "analogical_thinking": Technique.ANALOGICAL,
        "yes_and": Technique.YES_AND,
    }

    technique_key = params.technique.lower().replace(" ", "_")
    technique = technique_map.get(technique_key)

    if not technique:
        return json.dumps({
            "error": f"Unknown technique '{params.technique}'.",
            "available": list(technique_map.keys()),
        })

    prompt = get_technique_prompt(technique, params.topic)
    return json.dumps({
        "technique": params.technique,
        "topic": params.topic,
        "prompt": prompt,
    }, indent=2)


@mcp.tool(
    name="brainstorm_status",
    annotations={
        "title": "Get Current Brainstorming Session Status",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    }
)
async def brainstorm_status() -> str:
    """
    Returns the current state of the brainstorming session.
    Includes current phase, exchange count, and phase history.

    Returns:
        str: JSON with full session status
    """
    return json.dumps(_engine.get_status(), indent=2)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
