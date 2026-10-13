# UK Dating Statistic Calculator — agent instructions

Shared by every agent (Codex, Claude, Gemini/Antigravity). Keep this file lean: Codex auto-loads it every session; Claude and Gemini import it via CLAUDE.md / GEMINI.md. Do not re-read files your runtime already injected.

## Project
- Family: Otis — root: `N:\Otis Projects\UK dating statistic calculator` (drive letter may drift; locate by `Otis Projects\UK dating statistic calculator`)
- Plan: `docs/PLAN.md` (multi-step completion plan for the Next.js / React UK Dating Pool Calculator migration)
- Bundle: `- Base Prompts and Skill` at `N:\Otis Projects\- Base Prompts and Skill` (read-only)
- Env file: `\\100.125.189.51\SSD_GliNet\Otis Projects\- Base Prompts and Skill\.env` (found by `jev.py --check`; never print values)
- Build / run / test:
  - Unit tests: `npm test` (`src/lib/calculator.test.ts`)
  - Typecheck: `npx tsc --noEmit`
  - Lint: `npm run lint`
  - Dev server: `npm run dev`
  - Production build: `npm run build` (note: on SMB/UNC mounts, if Next build or npm install is slow, test/build from a local temp mirror or use `--webpack` flag)
- Project-specific rules:
  - Canonical stack is the Next.js 16 + React 19 + Tailwind CSS v4 + TypeScript app in `src/` (deployed to Vercel).
  - Legacy prototypes (`archive/streamlit_legacy/`, `archive/v3_legacy/`, `archive/temp-next-app/`) are archived and gitignored via `archive/`. Do not delete archived files.
  - Active evidence is `public/evidence/` with URL, table/query, reference period, geography and retained fingerprint. Preserve missing responses and suppression markers; normalize neither away.
  - Relationship status is one filter. Single means not living in a couple; legal divorce/widow status remains separate source taxonomy. Compute within sex/age strata, then sum; use observed qualification/ethnicity joint tables.
- Architecture: validated `calculatePool(input)` in `src/lib/calculator.ts`; test through `src/lib/calculator.test.ts`. Follow `docs/AUDIT-REMEDIATION.md` and ADR-002 for the superseding evidence/model decisions.
- Bug diagnosis: no speculative edits; always establish a tight reproducible verification loop (`diagnosing-bugs`) before fixing.
- Sensitive ops: generate interactive scripts (`wizard`) for human credential entry; never paste secrets in context.

## Hard rules
- Follow `BOOT.md` from the `- Base Prompts and Skill` bundle (locations, credentials, model limits, git safety, truthful reporting).
- That bundle is read-only. Never write into it; copy what you need into this project.
- Never put credentials, secrets or private keys in any file here; refer to variable names only.

## Per-prompt routing (JEV)
- For every new user prompt follow the bundle's `local-routing/README.md`: skip JEV for conversation, deterministic work and direct follow-ups; otherwise break the prompt into tasks, run `python "<bundle>/local-routing/jev.py" --runtime <runtime> --project . --prompt "..." --tasks ...`, and work inline / with one subagent / with parallel subagents as it decides (the user has authorized subagents). Override only with a stated reason.
- For multi-step tasks, synthesize specs (`to-spec`) and break into atomic tracer-bullet tickets declaring dependency edges (`to-tickets`: `blocked-by` / `blocking`) before subagent dispatch.
- Record JEV's pick and what you actually used in HANDOFF's `Routing` line. JEV unavailable: say so to the user in one line and use the same rules yourself.

## Resume & handoff
- `docs/HANDOFF.md` is the sole authoritative current-state snapshot. Overwrite stale state; keep it to about 60 lines.
- `docs/ACTIVE.md` (Wayfinder format: Destination, Frontier checklist `[x]`/`[~]`/`[ ]`, Fog-of-War, and Blockers) is used when the plan has more than five steps.
- `SHARED_NOTES.md` is a newest-first, append-only session log; each entry at most five lines: UTC, agent/model/effort, changes, verification, pointer. Rotate old entries to `docs/archive/` beyond about 200 lines.
- Never use `SHARED_NOTES.md` to determine current state. Read its top one or two entries only for a stale handoff or a specific history question.
- **/prime** (on every entry, even if you worked here before):
  1. Confirm the project root; read applicable instructions not already injected.
  2. Read `docs/HANDOFF.md`, and `docs/ACTIVE.md` if present.
  3. Run `git status --short`, `git diff --stat`, `git log --oneline -5`, and the Workspace ID command (in the HANDOFF.md comment).
  4. Compare Branch, HEAD, Tree and Workspace ID with HANDOFF.
  5. Any mismatch = work done after the last checkpoint: inspect only the affected paths and diffs, then proceed from the actual workspace. Never reset, clean, overwrite or force changes to match HANDOFF.
  6. Load only the files the next step needs. Resume work; no long orientation report.
- New project: `git init` unless the user forbids it. Existing non-git project: record touched paths instead of a Workspace ID.
- **Checkpoint** (rewrite HANDOFF): after each coherent work unit, before risky or lengthy work, and when quota/context may be running low. Quota can end a session without warning; the last checkpoint must be enough.
- **/handoff** (intentional exit): inspect task, workspace, relevant diff and test state; rewrite HANDOFF; update ACTIVE if used; add a SHARED_NOTES entry; record lasting architectural choices as ADRs in `docs/DECISIONS.md`.
- Do not auto-commit at handoff; commit only when project policy calls for it.
- `READY` means ready for a named review or decision. Mark tests passed, failed or not run; never claim unverified results.
