# Token Reduction Setup

Four open-source tools are installed **machine-wide** to cut how many tokens AI
coding agents burn. There is **nothing to install or configure in this project** —
the config lives in your home directory and applies to every folder you open.

This file is a reference copy placed in each project so the setup is discoverable
from wherever you happen to be working.

---

## The four tools

| Tool | What it cuts | Wired via | Automatic? |
|---|---|---|---|
| **RTK** | Shell/bash output the agent reads (input tokens) | Claude Code hook; `rtk` prefix elsewhere | Yes in Claude Code |
| **Headroom** | Large context payloads — JSON, logs, files | MCP server (+ optional proxy) | Partly — see caveats |
| **Caveman** | The agent's prose (output tokens) | Global rules + skill | Yes |
| **Ponytail** | The amount of code the agent writes (output tokens) | Global rules + skill | Yes |

They target different stages, so they stack rather than overlap:
RTK and Headroom shrink what goes **in**; Caveman and Ponytail shrink what comes **out**.

---

## How to use it

### Normal work
Nothing. Open any folder and the rules are already active.

### Useful commands

```bash
rtk gain
```

Shows how many tokens RTK has actually saved you, overall and per command.
This is the honest scoreboard — check it after a week of real work.

```bash
rtk proxy git status
```

Run one command **unfiltered**, when condensed output looks wrong or incomplete.

```bash
RTK_DISABLED=1 npm run build
```

Skip RTK entirely for a single command.

```bash
rtk discover
```

Finds past commands RTK could have condensed but didn't.

### Adjusting the agent's style

Both style tools have intensity levels — `lite`, `full` (default), `ultra`:

- `/caveman lite` — professional but tight, keeps full sentences
- `/caveman ultra` — maximum terseness
- `/ponytail ultra` — YAGNI extremist, challenges the requirement itself
- `stop caveman` / `normal mode` — back to normal prose
- `stop ponytail` — back to normal code

---

## What to realistically expect

Savings are **highly dependent on what you actually do**. Measured on a real
repo here, RTK gave:

| Command | Saved |
|---|--:|
| `ls -la app public` | 74.3% |
| `git log -n 25 --stat` | 0% |
| `grep -rn export app` | 0% |

RTK only compresses commands it has a filter for. Directory listings, test
output and `git status` compress well; unusual flag combinations pass through
untouched. A combined bench across a full task (shell + JSON reading + code
generation + explanation) measured roughly **70% total reduction**, but that
figure assumes a task mix that exercises all four tools.

Treat "80% savings" as a ceiling on a favourable workload, not a promise.

**Quality is not supposed to drop.** Caveman and Ponytail both carry explicit
guards: never compress away security warnings, irreversible-action
confirmations, input validation, error handling that prevents data loss, or
accessibility basics. If you ever see the agent cutting those, the skill is
misconfigured — check the files listed below.

---

## Caveats worth knowing

- **Claude Desktop bypasses Headroom's proxy.** The desktop app overwrites
  `ANTHROPIC_BASE_URL`, so proxy-based compression does not apply there. It works
  in the terminal `claude` CLI. Headroom's MCP tools are still available either way.
- **Headroom's text model downloads on first use.** Until it does, Headroom logs
  `Kompress model not ready` and prose compression silently does nothing. Its
  JSON compression works without it.
- **Codex needs the `rtk` prefix typed.** Codex has no pre-tool hook, so its rules
  instruct the agent to prefix commands itself. Claude Code does this automatically.
- **Restart after config changes.** Rules and skills load at session start.

---

## Where the config lives

| Path | What it is |
|---|---|
| `~/.claude/CLAUDE.md` | Global always-on rules (imports the three rule files) |
| `~/.claude/skills/caveman/`, `~/.claude/skills/ponytail/` | Full skills, on-demand |
| `~/.claude/settings.json` | RTK `PreToolUse` hook |
| `~/.codex/AGENTS.md` | Global rules for Codex (inlined, not imported) |
| `~/.gemini/config/rules/`, `~/.gemini/config/skills/` | Rules for Antigravity/Gemini |
| `~/.local/bin/rtk.exe`, `~/.local/bin/headroom.exe` | The binaries, on PATH |

Config backups are kept in `~/.claude/backups/`.

## Turning it all off

Delete or empty `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, and remove the
`PreToolUse` hook from `~/.claude/settings.json`. The binaries can stay — RTK does
nothing unless something calls it.

---

## Also installed: security skills

Two security skills from the ECC project are installed for all three agents
(Claude, Codex, Gemini). They are unrelated to token reduction — they are
documented here because this is the shared reference for global agent config.

| Skill | What it does |
|---|---|
| **security-review** | Checklist for *writing* secure code — secrets, input validation, SQL injection, authn/authz, XSS, CSRF, plus a cloud/infrastructure companion covering IAM, network and logging |
| **security-scan** | Audits your `.claude/` config itself — `CLAUDE.md`, `settings.json`, MCP servers, hooks and agent definitions — for secrets, over-permissive allow lists and injection risks |

`security-review` activates on its own when you touch auth, user input, secrets,
API endpoints or payment features. You can also call it by name.

**Naming difference on Claude Code:** Claude ships its own built-in
`security-review` (which reviews pending changes on the current branch). To keep
both, the ECC one is installed there as **`ecc-security-review`**. On Codex and
Gemini it keeps its original name. Ask for "ecc security review" in Claude, or
"security review" in the other two.

`security-scan` needs the AgentShield CLI, which is **not installed yet**:

```bash
npx ecc-agentshield scan
```

Two things to know before using it. Its `--opus` deep-analysis mode sends your
config to the Anthropic API and needs an `ANTHROPIC_API_KEY`. And `npx` pulls the
package fresh at run time — the same supply-chain pattern the scanner itself
flags as a finding. Pin it with `npm install -g ecc-agentshield` if that matters
to you.

---

## Sources

- RTK — https://github.com/rtk-ai/rtk
- Headroom — https://github.com/headroomlabs-ai/headroom
- Caveman — https://github.com/JuliusBrussee/caveman
- Ponytail — https://github.com/DietrichGebert/ponytail
- ECC security skills — https://github.com/affaan-m/ECC
- AgentShield — https://github.com/affaan-m/agentshield
