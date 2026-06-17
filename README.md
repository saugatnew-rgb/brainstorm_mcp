# BrainStorm MCP 🧠⚡

A brainstorming facilitator that plugs into Claude (and any MCP-compatible AI) to enforce **critical thinking discipline** — preventing premature closure, detecting surrender signals, and injecting productive friction.

> Designed by Dr Saugat Neupane, University of New England

---

## The Problem This Solves

When AI suggests something, people accept it too easily. It's the path of least resistance. This plugin **breaks that pattern** by:

- Never giving answers before the human commits to their own thinking
- Detecting when someone accepts an AI idea too quickly (surrender signals)
- Randomly injecting challenge questions, opposite views, or self-argue prompts
- Managing brainstorming phases so divergence happens before convergence
- Using established techniques: SCAMPER, Six Thinking Hats, Reverse Brainstorming, Analogical Thinking

---

## Install

```bash
pip install mcp fastmcp
```

---

## Run

```bash
python server.py
```

---

## Connect to Claude

In Claude Desktop, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "brainstorm": {
      "command": "python",
      "args": ["/path/to/brainstorm_mcp/server.py"]
    }
  }
}
```

---

## Tools

| Tool | What it does |
|---|---|
| `brainstorm_start` | Starts a session — AI asks only, no suggestions yet |
| `brainstorm_process` | Processes each human message — detects surrender, injects friction |
| `brainstorm_advance_phase` | Move to next phase (manual or auto) |
| `brainstorm_technique` | Apply SCAMPER, Six Hats, Reverse, etc. |
| `brainstorm_status` | See current phase and session state |

---

## The Six Phases

| Phase | What happens |
|---|---|
| **Frame** | AI asks only — no ideas yet |
| **Diverge** | Wild ideas, quantity over quality |
| **Provoke** | Deliberately wrong/opposite ideas |
| **Challenge** | Friction injection — nothing accepted easily |
| **Broaden** | Push beyond AI knowledge — human experience leads |
| **Synthesise** | Human connects the dots — AI only reflects |

---

## Files

```
brainstorm_mcp/
├── server.py       # MCP server — tools exposed to Claude
├── friction.py     # Surrender detection + friction injection
├── phases.py       # Phase engine + auto-detection
├── techniques.py   # SCAMPER, Six Hats, Reverse, etc.
└── README.md
```

---

## Licence

MIT — free to use, share, and extend.
