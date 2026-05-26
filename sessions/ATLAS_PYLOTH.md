# Pyloth Studio handoff — 2026-05-19

Repo: `~/Documents/pyloth` · main · last commit `e01f47c`
Live: `~/pyloth-studio/` on EC2 `i-021a93d3877298470` (Amazon Linux 2023, arm64), `63.183.201.253`, uvicorn at `127.0.0.1:8080`
Atlas working dir: `~/Documents/atlas`

## 1. Current objective

Building **Pyloth Studio** as the SA-facing UI for the scoping pipeline. Today's milestone (deadline **10:45 BG today**): demo a working "Plan" tab to **Vankata + Vova** showing how an SA would review a deliverable plan before chat-polishing it. Plan tab must look real (Neuralith design system), behave real (drag, toggle, click-to-preview), and be backed by a hand-curated `plan.json` for Garrett (no live planner yet).

Larger product context: `extract → discover → plan → review → build → iterate` pipeline. Today's work is the **review** surface.

## 2. What was completed

In commit order (each is a clean revert point):

| Hash | What |
|---|---|
| `d073883` | Pyloth Studio web layer: FastAPI, streaming Claude Code, file tree, mobile tabs, dual theme |
| `58f531d` | README rewrite: architecture (boxes), target pipeline (8-step user journey) |
| `8c40303` | Plan sub-tab v1: cards, drag, click-to-jump, eye toggle, unused catalog |
| `576033e` | Drop `Section N —` prefix from titles; stash garrett-plan.json as versioned fixture |
| `a1edcca` | Scripts to split deliverable HTML into tabs (Iris house style) |
| `df35185` | Click-to-jump uses postMessage, not hash reload |
| `f9328cc` | Plan redesign: story editor on top, split picked-list + inline preview iframe below |
| `2e8af28` | Fix split logic: cut at `<div class="section">` boundaries (cover was rendering blank from orphan divs) |
| `e01f47c` | Iframe absolute-positioned to fix 0-height under flex; Plan is now default sub-tab |

Pattern catalog discovery: `~/Documents/atlas/briefs/2026/W21/2026-05-19_pyloth-patterns-catalog.md` — 19 patterns from 17 engagements. Reviewed + cleaned (typo fixes, ID tightening, merged duplicate multilingual patterns). Not yet promoted to Pyloth repo as `src/pyloth/patterns/`.

## 3. Important architectural/context decisions

- **Hexagonal layers** preserved: `src/pyloth/interfaces/web/` is a new interface layer alongside `cli.py`. `pyloth studio --port 8080` CLI works. ruff per-file ignores added for the web layer (relaxed like infra).
- **Studio sits on the controller**, NOT the GPU instance. GPU = vLLM/Chandra worker, lifecycled by controller boto3.
- **Claude Code on controller** authed via Iris claude.ai workspace OAuth (Viktor blessed it for scoping work). No Bedrock, no API key. Token cached at `~/.claude/` on controller.
- **Naming hygiene rule (CRITICAL)**: never expose internal tech in client-facing deliverables — no Chandra, vLLM, GPT, OpenAI, Anthropic, run IDs, S3 paths. Map to **Axion** (extraction pipeline), **Neuralith** (data platform), **Iris.ai language models**. Memory: `iris-client-facing-naming.md`.
- **Publish target (planned, blocked on Rosen 2026-05-19)**: per-engagement vanity subdomain `garrett.iris.ai`. Today = S3 + signed URL. Memory: `pyloth-publish-strategy.md`.
- **plan.json source of truth**: runtime data on controller at `~/pyloth-studio/work/<engagement>/plan.json`. Repo fixture at `src/pyloth/interfaces/web/fixtures/garrett-plan.json` is the demo seed. Re-deploy with `scp`.
- **Deliverable HTML restructured into tabs**: `<div class="section">` boundaries became `<section class="pyloth-tab-pane">`. Idempotent script at `scripts/dev/split-deliverable-into-tabs.py`. Tab strip is sticky, fixed top, dark `#1c1c1c` + red accent `#c8102e`. Inline JS listens for `?section=...` query, `#hash`, and `postMessage({type:"pyloth-show-section",section})`.
- **Pattern catalog not yet wired**: today the plan is fully hand-curated. Be upfront about this in the Vankata+Vova call.

## 4. Files modified and why

| File | Why |
|---|---|
| `src/pyloth/interfaces/web/server.py` | FastAPI app. Endpoints: `/api/engagements`, `/api/state/{eng}`, `/api/files/{eng}`, `/api/file/{eng}?path=`, `/api/folder/{eng}?path=`, `/api/file-raw/{eng}?path=`, `/api/chat-stream/{eng}?message=` (SSE Claude Code stream), `/api/plan/{eng}`, `POST /api/plan/{eng}/story`, `POST /api/reset/{eng}`, `GET /preview/{eng}` serves deliverable HTML. Mounts `/static/`. |
| `src/pyloth/interfaces/web/static/index.html` | The whole Studio UI. Single-file: HTML + CSS (Neuralith DS: Saira/Poppins/Aber Mono, navy `#1c2550`, iris-violet `#3e4cd5`, light + dark themes) + vanilla JS. Sub-tabs: **Plan (default), Preview, Files**. Plan tab = story editor + picked-list + inline-section-preview-iframe. |
| `src/pyloth/interfaces/web/static/logo.png`, `fonts/Aber-Mono-*.woff2` | Pyloth crystal logo + Neuralith mono font. |
| `src/pyloth/interfaces/web/fixtures/garrett-plan.json` | Hand-curated plan for the Garrett demo. 7 picked sections (cover + 6), 14 available-but-unused (mix of optional + skipped) with rationale and `would_enable_at` triggers. `story` field is editable in UI. |
| `src/pyloth/interfaces/cli.py` | Added `pyloth studio --host --port --work-root` command. |
| `pyproject.toml` | Added `[web]` optional extras (fastapi, uvicorn[standard], pydantic); per-file ruff ignores for web layer; mypy relaxed for `pyloth.interfaces.web.*`; setuptools package-data for static/fonts. |
| `README.md` | Rewrote Architecture (boxes/deps mermaid) + Target pipeline (8-step journey mermaid). |
| `scripts/dev/add-deliverable-anchors.py` | Inject anchor `<div id="section-XX-...">` into legacy single-page deliverable HTML. Idempotent. |
| `scripts/dev/split-deliverable-into-tabs.py` | Transform anchored HTML into multi-tab pyloth-tab-pane shell. Idempotent; backs up to `.pre-tabs.bak`. |

## 5. Current blockers/issues

**LIVE BUG (probably fixed in `e01f47c`, awaiting user confirmation)**: Plan tab inline section-preview iframe was rendering white. Likely root cause: iframe under flex chain had 0 effective height. Fixed with `position: absolute; inset: 0` + `min-height: 320px` on `.plan-split-right-body`. **User was hard-refreshing to verify when conversation ended.** If still broken: check `#plan-preview-iframe` computed style in devtools (width/height/position), and confirm `.plan-preview-empty.gone` is being set when a card is clicked (CSS `display: none` should kick in).

**Demo at 10:45 today is the deadline.** Per local time when this was written, runway was ~2.5 hours. Plenty of slack but don't introduce big refactors.

**Pending question, raised but not yet implemented**: User asked "can the plan section be a separate first window which shows first but we can go back to it (so it's more about structure)". This is a bigger structural change — Plan becomes a full-page landing screen on engagement load, with "Approve plan" routing to the chat-and-preview Studio view. NOT for today's demo. Discuss with Vankata + Vova as the next iteration.

## 6. Exact next steps

In priority order:

1. **Confirm iframe bug is fixed** by asking user to hard-refresh and click a picked section card. If still white, devtools inspection needed.
2. **Test the live demo end-to-end** before 10:45:
   - Plan tab opens by default with Garrett engagement
   - 7 picked sections visible, drag works, eye toggle works
   - Click any card → that section renders in right-hand iframe (NOT in Preview tab)
   - "Fullscreen" button in section-preview header → switches to Preview tab with that section active
   - Catalog drawer expands → 14 unused patterns visible with rationale
   - Click optional card → promotes to picked
   - Story textarea autosaves on blur (visible "Saved" indicator)
   - Preview tab → tabbed multi-section HTML works (Overview / Documents / For Feras / Schema / For Norbert / Gaps / Pipeline)
   - Theme toggle works (light = Neuralith on-brand, dark = cinematic)
3. **Don't break anything** before the call. Polish, don't refactor.
4. **After the call**: tackle the "Plan as separate first window" structural ask. Sketch with user, then ~1-2 hours implementation.
5. **Pattern catalog promotion**: copy `~/Documents/atlas/briefs/2026/W21/2026-05-19_pyloth-patterns-catalog.md` into `pyloth/src/pyloth/patterns/PATTERNS.md` + scaffold one folder per pattern (id, yaml, prompt fragment, canonical example) — when user confirms catalog is locked.

## 7. Commands needed to continue

**SSH to controller:**
```
ssh -i ~/.ssh/pyloth-controller ec2-user@63.183.201.253
```

**SSH tunnel for browser access (user runs this in a separate terminal — currently open):**
```
ssh -L 0.0.0.0:8080:localhost:8080 -i ~/.ssh/pyloth-controller ec2-user@63.183.201.253
```
Then browser at `http://localhost:8080`. Phone (same LAN) at `http://<laptop-LAN-ip>:8080`.

**Restart uvicorn on controller (real PID, not pattern match — pkill catches the SSH session):**
```
ssh -i ~/.ssh/pyloth-controller ec2-user@63.183.201.253 'ps -ef | grep "[u]vicorn" | awk "/python3 .venv/ {print \$2}"'
# Then kill that exact PID, restart:
ssh -i ~/.ssh/pyloth-controller ec2-user@63.183.201.253 'kill <PID>; sleep 1; cd ~/pyloth-studio && nohup .venv/bin/uvicorn server:app --host 127.0.0.1 --port 8080 > /tmp/pyloth-studio.log 2>&1 < /dev/null & disown'
```

**Deploy frontend change:**
```
scp -i ~/.ssh/pyloth-controller /Users/iris/Documents/pyloth/src/pyloth/interfaces/web/static/index.html ec2-user@63.183.201.253:/home/ec2-user/pyloth-studio/static/index.html
# No restart needed for static files.
```

**Deploy server change (requires restart):**
```
scp -i ~/.ssh/pyloth-controller /Users/iris/Documents/pyloth/src/pyloth/interfaces/web/server.py ec2-user@63.183.201.253:/home/ec2-user/pyloth-studio/server.py
# Then restart uvicorn per above.
```

**Lint before commit:**
```
cd /Users/iris/Documents/pyloth && .venv/bin/ruff check src/pyloth/interfaces/web/
```

**Run tests:**
```
cd /Users/iris/Documents/pyloth && source .venv/bin/activate && pytest tests/unit -q
```

**Smoke-test endpoints from controller:**
```
ssh -i ~/.ssh/pyloth-controller ec2-user@63.183.201.253 \
  'curl -s http://127.0.0.1:8080/api/plan/garrett | python3 -m json.tool | head -30'
```

**Revert points if anything broken:**
```
cd /Users/iris/Documents/pyloth
git log --oneline -10            # see hashes
git reset --hard <hash>          # local rollback
# To revert deliverable HTML: restore from controller backup:
ssh -i ~/.ssh/pyloth-controller ec2-user@63.183.201.253 \
  'cp ~/pyloth-studio/work/garrett/deliverable/index.html.pre-tabs.bak ~/pyloth-studio/work/garrett/deliverable/index.html'
```

## 8. Assumptions/warnings

- **No git push without explicit user request.** User asks for commits; they're the gate.
- **Never auto-send outward-facing comms** (Slack, email, calendar). Draft → user approves → send.
- **`pkill -f "uvicorn"` kills the SSH session too** because the command string matches the shell command running on the remote. Always use exact PID instead.
- **plan.json on controller is the live source**; my `POST /api/plan/{eng}/story` overwrites it. Smoke-testing that endpoint will overwrite the story (I did this once during a test — re-deployed from `/tmp/garrett-plan.json` to restore). The repo fixture stays clean only because I `scp` the user-blessed version separately.
- **Aber Mono font** is self-hosted under `static/fonts/`. If a deploy misses these the Neuralith look breaks.
- **Iframe sandbox**: not currently set. Deliverable HTML is trusted (we generate it). Don't add `sandbox=""` without thinking — it'd break the postMessage / inline JS in the deliverable.
- **The 8-page Garrett demo** is token 111 in Neuralith dev DB (`description: "Pyloth Test"`). Extraction outputs at `s3://iris-engagements/pyloth-test/` were wiped earlier; current outputs live in `~/pyloth-studio/work/garrett/` on the controller.
- **Anthropic API key**: Iris doesn't have a workspace key. We use the **Iris claude.ai workspace OAuth** for Claude Code on the controller. Borislava's Bedrock recipe is on file (Slack thread `1778689428.250439`) but not used here.
- **No emojis in code, UI, or commit messages** unless user explicitly requests.
- **House style**: terse > grammatical, no em-dashes (use commas/colons/parens), no trailing "what I did" summaries. Client-facing artifacts: no internal paths/repo names/tool names.
- **The atlas memory index** at `~/.claude/projects/-Users-iris-Documents-atlas/memory/MEMORY.md` loads each session. Skim it for Ivo's voice, working hours, escalation patterns.

## 9. Git status summary

**Repo `~/Documents/pyloth`**: clean working tree, `main` up to date with `origin/main` at `e01f47c`.

Recent commits:
```
e01f47c Studio: Plan inline preview iframe absolute positioning + Plan default tab
2e8af28 fix: split deliverable at <div class=section> boundaries
f9328cc Studio: redesign Plan tab — story + split layout
df35185 Studio: click-to-jump postMessage
a1edcca dev: deliverable tab-split scripts
576033e Studio: drop "Section N —" title prefix + stash plan fixture
8c40303 Studio: Plan sub-tab v1
58f531d README: rewrite architecture + target pipeline diagrams
d073883 Pyloth Studio web interface (initial)
8fd2d50 Chandra v2: ocr_layout-style prompt + per-page outputs
```

**Repo `~/Documents/atlas`**: not a git repo for code, but memory + brief files are checkpointed. Latest atlas writes:
- `briefs/2026/W21/2026-05-19_pyloth-patterns-catalog.md` (the 19-pattern catalog from the recon agent)
- `~/.claude/projects/-Users-iris-Documents-atlas/memory/iris-client-facing-naming.md` (mandatory naming rule)
- `~/.claude/projects/-Users-iris-Documents-atlas/memory/pyloth-publish-strategy.md` (subdomain plan)

**Controller `/home/ec2-user/pyloth-studio/`**: in sync with repo at `e01f47c`. Live uvicorn running. Recent server log clean. Engagement working dir `work/garrett/` has `brief.yaml`, `plan.json`, `inputs/`, `deliverable/index.html` (multi-tab version), `deliverable/index.html.pre-tabs.bak` (pre-tab-split fallback), `chat-history.json`, `.claude-session-id`.
