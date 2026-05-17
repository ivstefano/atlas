---
description: Bootstrap a new engagement folder. Scaffolds the 5-file structure under engagements/_pending/ (or engagements/ if confidence is high), seeds CONTEXT/STATUS/COMMERCIAL/SOURCES/ARTEFACTS, adds entry to _aliases.yaml. Asks 5 targeted questions before writing anything.
argument-hint: <company-name> [trigger-context]
---

# New engagement bootstrap

Scaffold a new engagement at `engagements/<slug>/` (or `engagements/_pending/<slug>/` if uncertainty), from the 5-file template at `engagements/_template/`.

**Arguments**:
- `$1` = company name (required, e.g. "Acme Logistics" — will be slugified to `acme-logistics`)
- `$2+` = optional trigger context (e.g. "Calendar event Tue 3pm with john@acme.com", "Jordan email thread", "asked by Vankata")

If no `$1` provided: ask the user for the company name and stop. Don't guess.

## Step 1 — confirm scope before writing anything

Before scaffolding, run `AskUserQuestion` to gather the irreducible 5 pieces of info that the template can't infer. Phrase questions concisely. **Always offer 2-3 concrete options + an "Other" escape.** Acceptable to ask all 5 in one batch.

**The 5 questions** (combine into one AskUserQuestion call, keep each header ≤12 chars):

1. **Lead source** — how did this engagement come in?
   - Options: `Inbound (Jordan pipeline)`, `Outbound (Steven/Viktor)`, `Conference / event`, `Existing client referral`
2. **Stage now** — where are we today?
   - Options: `lead-in (Jordan only, no Ivo yet)`, `intro (intro call booked)`, `pre-scoping (Ivo enters)`, `scoping (work started)`
3. **Type (initial guess)** — even rough.
   - Options: `axion-extraction (unstructured docs)`, `rag (queryable DB + agent)`, `hybrid`, `TBD`
4. **Folder destination** — confident enough to skip `_pending/`?
   - Options: `Confident → engagements/<slug>/`, `Uncertain → engagements/_pending/<slug>/`
5. **One-line use case** — what is the client trying to do, in plain words?
   - Free text (no preset options)

**Skip the protocol** if the user prefix-passes them: e.g. `/new-engagement Acme inbound pre-scoping axion confident "extract specs from RFPs"` parses positionally. Otherwise ask.

## Step 2 — check for name collisions

Before writing:

- Read `engagements/_aliases.yaml`. If the slugified name matches an existing key OR if any alias / domain / title in the file matches what the user said → **stop**, surface the match, ask if they meant the existing engagement.
- Check `engagements/<slug>/` and `engagements/_pending/<slug>/` exist already. If yes → stop, ask user.

## Step 3 — scaffold

Slugify: lowercase, replace spaces / `&` / `/` with `-`, strip non-alphanumeric except `-`. Example: `Taylor & Francis` → `taylor-francis`. **But** check `_aliases.yaml` for established conventions (e.g. `tandf`, `sms-group`, `deutschebahn`) — use that slug instead if a match is obvious.

Then:

1. `cp -r engagements/_template engagements/<dest>/<slug>` where `<dest>` is empty (`engagements/`) or `_pending`.
2. Sed-replace all `{{COMPANY}}` → display name (e.g. "Acme Logistics"), `{{TODAY}}` → today's ISO date, `{{LEAD_SOURCE}}` → answer to Q1, `{{INTRODUCED_BY}}` → Jordan if "inbound", else Steven/Viktor/etc., `{{ONE_PARAGRAPH_SUMMARY}}` → answer to Q5, `{{OPENING_NOTE}}` → trigger context from `$2+`, `{{NEXT_ACTION}}` → "first call: <date or TBD>", `{{NEXT_ACTION_BY}}` → "this week" if no specific date known.
3. Set `Stage:` in `CONTEXT.md` to the answer from Q2.
4. Set `Type:` in `CONTEXT.md` to the answer from Q3.
5. Remove `.DS_Store` from the copied folder.

## Step 4 — register alias

Append entry to `engagements/_aliases.yaml`. Insert alphabetically among active engagements (not in the `_internal:` or tombstone sections at the bottom). Format:

```yaml
<slug>:
  status: active        # or pre-scoping for early-stage
  domains: []           # ask user if a domain is known yet; otherwise []
  titles:
    - <Display Name>
    - <Short alias if any>
```

If a domain was mentioned in the trigger context (`$2+`), include it; otherwise leave `domains: []` and note in the report that the user should fill it in after the first call.

## Step 5 — Asana section

Note in the final report (do NOT auto-create):

> Asana section in `Iris.ai Commercial Engagements` (project GID `1214855342290138`) not auto-created. Create manually if engagement looks real — per Viktor 2026-05-15 state lives in Asana + HubSpot.

(Future enhancement: once Asana MCP write-confidence is higher, this step creates the section automatically.)

## Step 6 — commit

```bash
cd /Users/iris/Documents/engagements
git add <dest>/<slug>/ _aliases.yaml
git commit -m "new engagement: <Display Name> (<stage>)"
```

Do NOT push (engagements is bitbucket, push requires explicit user OK).

## Step 7 — report to user

Single terse message. Format:

```
Scaffolded: engagements/<dest>/<slug>/
  Stage: <stage>  Type: <type>  Lead: <lead source>
  CONTEXT.md, STATUS.md, COMMERCIAL.md, SOURCES.md, ARTEFACTS.md, _briefs/, 1_pre-scoping/ all seeded
  _aliases.yaml entry added (domains: <list or "empty — fill after first call">)

Asana: section NOT auto-created (manual: project 1214855342290138, add section "<Display Name>")
HubSpot: not wired yet — Jordan creates the deal there

Commit: <hash>. Not pushed (do manually if pushing to Bitbucket).

Next actions you might want:
  - Fill domain in _aliases.yaml after first email exchange
  - If in _pending/: promote to engagements/<slug>/ after Ivo confirms it's real
  - Add Asana section if commercial-tracker-worthy
```

## Constraints

- **Never** scaffold without confirming the 5 questions (unless prefix-passed in `$1+`).
- **Never** auto-write the alias entry if there's a possible collision — flag and stop.
- **Never** auto-create the Asana section (write-side trust not established yet).
- **Never** push to remote.
- If user says "abort" or "stop" during the AskUserQuestion: cancel; remove nothing (you haven't written anything yet at that point).

## Edge cases

- **Closed-lost / tombstone scaffolding**: if user says "this is a tombstone, just record the loss" → skip Q2/Q3, set Stage: `closed-lost` or `closed-paused`, write a 3-line STATUS entry explaining why, skip _aliases.yaml entry (or put under tombstone section at bottom).
- **Existing `_pending/` engagement getting promoted**: this slash command is for NEW; promotion is a manual `mv engagements/_pending/<slug> engagements/<slug>` + alias `status: pre-scoping` → `active` flip.
- **`/new-engagement` from a Calendar event with no human in the loop**: this slash command always pauses for the 5 Qs. The morning brief flags unmatched events but does NOT call this command automatically (per morning-brief.md constraint "Never auto-create a new engagement folder").
