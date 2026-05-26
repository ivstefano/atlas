# Handoff: atlas LinkedIn drafting workflow

**Date:** 2026-05-19
**Skill in use:** superpowers:brainstorming (mid-flow, dry-run phase)

## 1. Current objective

Build a low-overhead workflow in atlas for Ivo to draft LinkedIn posts under his own name. Personal brand + Iris.ai traffic. Quality + consistency over volume. Manual posting v1, HubSpot deferred.

## 2. What was completed

- Brainstorming dialogue done (5 clarifying questions answered).
- Design approved by Ivo across 4 sections (architecture, voice audit, slash command, folder layout + build order).
- Spec written and committed: `docs/superpowers/specs/2026-05-19-linkedin-drafting-workflow-design.md` (commit `1a894c2`).
- Ivo reviewed spec, said "okay looks good, let's dry run".
- Started dry-run (simulating `/li-post` without building it). Answered Q1 (topic = DB scoping demo lessons). Was about to ask Q2 (source tag) when Ivo interrupted to request this handoff.

## 3. Architectural / context decisions

- **Drafting lives in atlas**, not Claude.ai project, not HubSpot AI. Voice memories + claude-mem context already here, free to reuse.
- **Voice file at `_voice/li.md`** (not repo root), anticipating siblings `_voice/email.md`, `_voice/talk.md` later. Decided 2026-05-19.
- **Posts at `atlas/posts/`** for now (Ivo confirmed). atlas is private to Ivo, no concern about exposing drafts.
- **Skip existing LinkedIn post history** for voice audit. Ivo has a few posts, nothing representative.
- **Voice audit inputs:** Slack samples (reuse [[slack-self-audit-2026-05-18]]), Tactiq transcripts, existing memories ([[ivo-voice-profile]], [[email-drafting-style]], [[comms-style-improvements]]).
- **No HubSpot, no scheduler in v1.** Manual posting only. Automation deferred until voice trusted.
- **Build order:** voice audit → 3 validation drafts → /li-post command → first real post → (later) HubSpot.
- **5 structural templates:** story-with-lesson, contrarian-take, behind-the-scenes, technical-explainer, industry-comment.

## 4. Files modified and why

- `docs/superpowers/specs/2026-05-19-linkedin-drafting-workflow-design.md` — created and committed (`1a894c2`). The approved design.
- `sessions/ATLAS_LI.md` — this handoff, just created.

No other repo files touched in this thread. The pre-existing `M`/`??` items in git status are from prior work (auto brief, slack self-audit brief, pyloth-patterns-catalog), unrelated to LI workflow.

## 5. Current blockers / issues

- None blocking. Ivo wanted to dry-run the `/li-post` flow (role-play it without building) before committing to writing-plans. We were in question 2 of 3 of the simulated `/li-post`.

## 6. Exact next steps

When resuming:

1. **Resume the dry run.** Ask Ivo Q2: source tag for the DB scoping demo post. Options: `db-infrago` (engagement-specific) / `industry` (industry commentary using DB as trigger) / `meta` (about IRIS scoping practice in general).
2. Ask Q3: which template (story-with-lesson / contrarian / behind-the-scenes / technical / industry-comment / let-AI-pick).
3. Pull context: claude-mem search for "DB scoping demo", read `engagements/db-infrago/STATUS.md` if exists, read [[db-infrago-deal]] memory, the three voice memories, and (since `_voice/li.md` does not exist yet) operate with just the existing voice memories as a stand-in.
4. Draft 2-3 variants in chat. Iterate with Ivo.
5. After dry run: ask if design holds, then invoke `writing-plans` skill to write the implementation plan for the actual build.

**Do NOT skip to writing-plans without finishing the dry run.** Ivo explicitly asked for it.

## 7. Commands needed to continue

```bash
# Verify spec exists
cat /Users/iris/Documents/atlas/docs/superpowers/specs/2026-05-19-linkedin-drafting-workflow-design.md

# Context lookups during dry run
ls /Users/iris/Documents/engagements/db-infrago/ 2>/dev/null
cat /Users/iris/.claude/projects/-Users-iris-Documents-atlas/memory/db-infrago-deal.md
cat /Users/iris/.claude/projects/-Users-iris-Documents-atlas/memory/ivo-voice-profile.md
cat /Users/iris/.claude/projects/-Users-iris-Documents-atlas/memory/email-drafting-style.md
cat /Users/iris/.claude/projects/-Users-iris-Documents-atlas/memory/comms-style-improvements.md
```

Use claude-mem skill (`mem-search`) to pull recent DB scoping demo observations if needed.

## 8. Assumptions / warnings

- Ivo prefers terse, no em-dashes, no AI-tell phrasing. Memory [[email-drafting-style]] applies to drafts.
- House Style (global CLAUDE.md): no em-dashes, no emojis unless requested, terse over grammatical.
- Brainstorming skill HARD-GATE: do NOT invoke any implementation skill (writing-plans, frontend-design, etc.) until dry run done and Ivo explicitly approves moving to plan.
- Voice file `_voice/li.md` does NOT exist yet. Dry run uses existing voice memories as stand-in.
- `posts/` directory does NOT exist yet. Dry run doesn't write files, just role-plays the chat-side of `/li-post`.
- Ivo's date today: 2026-05-19.
- Ivo's working dir: `/Users/iris/Documents/atlas`.
- atlas is private. Engagements at `~/Documents/engagements/` (separate repo).

## 9. Git status summary

**Branch:** `main` (clean for our work — spec committed as `1a894c2`).

**Pre-existing uncommitted items (not ours, leave alone):**
```
 M NEXT_PRIORITIES.md
 M briefs/2026/W21/2026-05-18_auto.md
 M briefs/2026/W21/2026-05-18_slack-self-audit.md
?? .claude/scheduled_tasks.lock
?? Neuralith Design System/
?? _assets/
?? briefs/2026/W21/2026-05-19_pyloth-patterns-catalog.md
```

**Our commit:**
```
1a894c2 spec: linkedin drafting workflow in atlas
```

No PR. atlas is local-only ops repo.
