# LinkedIn drafting workflow in atlas

**Date:** 2026-05-19
**Owner:** Ivo
**Status:** approved (design); pending implementation

## Goal

Ship a low-overhead workflow for Ivo to post on LinkedIn under his own name with consistent voice and cadence. Output is personal-brand reach and traffic to Iris.ai. Quality and consistency over volume. Manual posting in v1; HubSpot scheduling deferred until voice is trusted.

## Non-goals

- Marketing automation for Iris.ai (Ada owns that).
- Multi-author publishing pipeline (Karina / content agency flow).
- Visuals / image generation.
- Auto-posting via LinkedIn API.
- HubSpot integration in v1.

## Architecture

Three artefacts inside atlas, no external systems:

- `_voice/li.md` — voice memory built from a one-time audit. Locked do/don't lists, structural templates, phrase bank. Future siblings (`_voice/email.md`, `_voice/talk.md`) anticipated but out of scope.
- `posts/YYYY-MM-DD_<slug>.md` — one file per post. Frontmatter (status, source, template, posted_at) + body. Committed to atlas.
- `.claude/commands/li-post.md` — slash command that asks for topic + source + template, pulls context, drafts 2-3 variants, saves the chosen draft to `posts/`.

Posting is manual. Copy from approved file into LinkedIn.

## Folder layout

```
atlas/
├── _voice/
│   └── li.md                             # voice memory
├── posts/
│   ├── README.md                         # status legend, conventions
│   ├── 2026-05-20_<slug>.md
│   └── ...
└── .claude/commands/
    └── li-post.md
```

## Components

### 1. Voice memory (`_voice/li.md`)

Built once via a structured audit before the slash command is useful.

**Inputs:**
- Slack samples (reuse [[slack-self-audit-2026-05-18]] findings)
- Tactiq transcripts where Ivo explains things at length
- Existing memories: [[ivo-voice-profile]], [[email-drafting-style]], [[comms-style-improvements]]
- Existing LinkedIn posts: skipped (Ivo has a few, not representative)

**Extraction:**
- Register (casual / analytical / contrarian)
- Sentence length distribution
- Hook style preferences (question / claim / story)
- Open and close patterns
- Phrases Ivo uses and phrases he never uses
- Emoji posture
- Hashtag posture
- Gap: Slack voice (internal, terse) → LinkedIn voice (more setup for outsiders)

**Output:** locked `_voice/li.md` with:
- Do-list
- Don't-list
- 5 structural templates: story-with-lesson, contrarian-take, behind-the-scenes, technical-explainer, industry-comment
- Phrase bank
- Example openings and closings

**Validation:** generate 3 test posts on known topics (DB scoping demo, Pyloth naming, Agrolimen closed-lost lesson). Ivo reacts. Tune the voice doc until drafts feel like him.

### 2. Posts folder (`posts/`)

One markdown file per post. Frontmatter:

```yaml
---
topic: <slug>
source: <engagement-key | 'industry' | 'meta'>
template: story-with-lesson | contrarian | behind-the-scenes | technical | industry-comment
status: draft | approved | posted
posted_at: null | YYYY-MM-DD
---
```

Status flow: `draft` → `approved` → `posted`. Manual update of `posted_at`.

`posts/README.md` documents the legend and notes this is personal-brand drafting, not Iris marketing.

### 3. Slash command (`/li-post`)

**Trigger:** user runs `/li-post`.

**Behavior:**

1. Ask 3 questions via AskUserQuestion:
   - Topic / angle (free text)
   - Source: DB / Pyloth / Garrett / Agrolimen / industry / other
   - Template: one of the 5 templates, or let-AI-pick

2. Pull context automatically:
   - `_voice/li.md` (always)
   - [[ivo-voice-profile]], [[email-drafting-style]], [[comms-style-improvements]] (always)
   - claude-mem search for topic keywords
   - Engagement STATUS.md if a source engagement was named
   - Last 5 files in `posts/` (avoid repeated angles, hooks, openings)

3. Draft 2-3 variants in chat. Differ on hook / length / angle. Same topic.

4. User picks one or says "redo, more X". Iterate.

5. On "save", write to `posts/YYYY-MM-DD_<slug>.md` with frontmatter `status: approved`, `posted_at: null`.

6. Tell user to post manually and update `posted_at` later.

No HubSpot, no scheduler in v1.

## Build order

1. Voice audit → produces `_voice/li.md`.
2. Validation: 3 test drafts on known topics. Iterate voice doc.
3. Build `/li-post` slash command using validated voice doc.
4. First real post.
5. Deferred: HubSpot scheduling once Ivo trusts the drafts.

## Success criteria

- After voice audit + validation, 3 test drafts feel like Ivo without manual rewriting.
- `/li-post` produces draftable variants in under 2 minutes of interaction.
- Cadence sustainable at 1-3 posts/week without dread.

## Out of scope (deferred)

- HubSpot scheduling integration.
- Visual / image generation.
- Auto-tracking of posted_at via LinkedIn API or scraping.
- Other voice profiles (`_voice/email.md`, `_voice/talk.md`).
- Cross-posting to other platforms.

## Memory updates

After implementation:
- Add `_voice/li.md` entry to `MEMORY.md` so it's discoverable next session.

## Unresolved questions

None at this point. Ready for implementation plan.
