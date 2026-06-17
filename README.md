# BrainStorm MCP 🧠⚡

> Most AI tools make thinking easier. This one makes it harder — on purpose.

BrainStorm MCP is a brainstorming facilitator that plugs into Claude (and any MCP-compatible AI) to enforce **critical thinking discipline** — preventing premature closure, detecting surrender signals, and injecting productive friction.

> Designed by Dr Saugat Neupane

---

## Why I Built This

I use Claude and other AI tools every day — to build tools, create artefacts, brainstorm ideas.

But recently, when I stopped and reflected, I noticed something uncomfortable. I was slowly surrendering to it. Not dramatically. Quietly. I'd ask, it would respond, and I'd just... accept it. Move on.

Because questioning takes effort. Accepting is easy. And we've all been there.

That realisation bothered me — because thinking critically is literally what I do as a university lecturer. So I built something to stop myself from doing it.

---

## The Problem It Solves

When AI suggests something, people accept it too easily. This plugin **breaks that pattern** by:

- Never giving answers before the human commits to their own thinking
- Detecting when someone accepts an AI idea too quickly (surrender signals)
- Injecting productive friction — challenge questions, opposite views, reverse brainstorming
- Managing brainstorming phases so divergence happens before convergence
- Using established techniques: SCAMPER, Six Thinking Hats, Reverse Brainstorming, Analogical Thinking

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

## How to Install & Connect to Claude Desktop

### Step 1 — Make sure Python is installed
Open your terminal (Mac/Linux) or Command Prompt (Windows) and run:python --version
You need Python 3.8 or higher. If not installed, download from https://python.org

---

### Step 2 — Download this repo
Click the green **Code** button at the top of this page → **Download ZIP**

Unzip it somewhere easy to find, for example your Desktop.

---

### Step 3 — Install dependencies
Open your terminal, navigate into the unzipped folder, and run:pip install mcp fastmcp
---

### Step 4 — Find your Claude Desktop config file
Claude Desktop stores its settings here:

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Open that file in any text editor (Notepad on Windows, TextEdit on Mac).

---

### Step 5 — Add BrainStorm MCP to the config
Paste this into the config file. Replace the path with wherever YOU saved the folder.

**Windows example:**
```json
{
  "mcpServers": {
    "brainstorm": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\Desktop\\brainstorm_mcp\\server.py"]
    }
  }
}
```

**Mac example:**
```json
{
  "mcpServers": {
    "brainstorm": {
      "command": "python",
      "args": ["/Users/yourname/Desktop/brainstorm_mcp/server.py"]
    }
  }
}
```

> If your config file already has other MCP servers, just add the `"brainstorm"` block inside the existing `"mcpServers"` section — don't replace the whole file.

---

### Step 6 — Restart Claude Desktop
Close Claude Desktop completely and reopen it. The brainstorm tools will now be available.

---

### Step 7 — Test it
In Claude, just say:
> *"Start a brainstorm session about [your topic]"*

Claude will use BrainStorm MCP automatically from there.

---

## Tools

| Tool | What it does |
|---|---|
| `brainstorm_start` | Starts a session — AI asks only, no suggestions yet |
| `brainstorm_process` | Processes each message — detects surrender, injects friction |
| `brainstorm_advance_phase` | Move to next phase manually or auto |
| `brainstorm_technique` | Apply SCAMPER, Six Hats, Reverse Brainstorming, etc. |
| `brainstorm_status` | See current phase and session state |

---

## Files
---
brainstorm_mcp/

├── server.py       # MCP server — tools exposed to Claude

├── friction.py     # Surrender detection + friction injection

├── phases.py       # Phase engine + auto-detection

├── techniques.py   # SCAMPER, Six Hats, Reverse, etc.

└── README.md

## Licence

MIT — free to use, share, and extend.
