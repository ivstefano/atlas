---
description: Draft an email as Ivo (reply or new) into a real Gmail draft in the right thread, with checked recipients, current facts and confirmed attachments. Never sends.
argument-hint: <Gmail thread link | subject | person> <what the email should say>   (or: new <person/engagement> <intent>)
---

# /email

Draft an email Ivo will send. Input: `$ARGUMENTS` = a Gmail thread link, a subject, or a person, plus the intent. `new ...` means a fresh email, no thread.

The output is a **Gmail draft in the same thread** plus a preview in chat. Nothing is ever sent.

Why this command exists: Ivo corrected about 65% of email drafts. Top causes: wrong recipients, cc or threading; the draft stayed in chat or the connector was down; missing content or attachment; stale facts; too long or AI-sounding. Each step below closes one of those.

## Hard rules

- Never call `mcp__gcal__send_gmail_message`. Draft only.
- Never attach a file without Ivo saying yes to that file.
- Cc everyone involved, **including people who are away** (Ivo's rule for email: cc them even on PTO). This overrides the autopilot `drop_away_emails` behaviour, which applies to generated digests only. Away people are not addressed in the opener and not given next steps; their cover is.
- Jordan's address is `jordan_ryken@iris.ai`. Replace any `jordan.ryken@` (it bounces).
- Never draft Jordan's own commercial replies (pricing, SoW, contract or NDA terms, AWS funding, reschedules of meetings he owns). Say "Jordan owns this" and stop. While he is away, name the cover from the away list (step 4) and stop unless Ivo says the slice is his.
- Client-facing naming: Axion, Neuralith, Iris.ai models. No Chandra, vLLM, GPT, run IDs, S3/EC2, repo or tool names (memory `iris-client-facing-naming`).
- Plain typography: no em or en dashes, arrows, fancy quotes, ellipsis glyph, `~`, bold or bullet glyphs.

## Steps

### 0. Load the voice first

Before reading the thread, invoke the `ivo-voice` skill (email row: `voice_written.json`, `voice_spoken.json`, email section of memory `ivo-voice-profile`), then the `human-writing` skill. Not optional; do not draft without both.

### 1. Find the real thread

- Gmail link: the id after `#inbox/`, `#all/`, `#sent/` etc. Try `mcp__gcal__get_gmail_thread_content(thread_id=<id>, include_analysis=true)`. If that fails, the id may be a message id: `get_gmail_message_content`, take its thread id, retry.
- Subject or person: `mcp__gcal__search_gmail_messages(query=..., include_headers=true, page_size=10)` (for example `subject:"final results" newer_than:30d`, or `from:gerome OR to:gerome newer_than:30d`). One clear hit: use it. Several: list the top 3 (subject, last sender, date) and ask which.
- `new`: no thread. Recipients come from the engagement CONTEXT stakeholders (step 3). Search Gmail once for an existing thread on the same topic first; replying in it beats a new thread.

### 2. Read the thread properly

From the full thread:
- The **last real message**. Skip reactions ("X reacted to your message"), auto-replies, out-of-office notes and calendar notices. If the last message is one of those, say so: "Gerome only reacted with a heart, nothing to answer. Still want to write?" Gmail's ball-in-court analysis counts reactions as replies; don't trust it blindly.
- Who asked what, and which question the email answers.
- Ivo's own last message in the thread: copy its sign-off block and title exactly (his real one, for example "Best,\nIvo Stefanov\nSenior Solutions Architect\nIris.ai | ivo@iris.ai"). In established threads with short replies, "Best,\nIvo" is fine.
- The full participant list: From, To and Cc of every message, plus `analysis.participants`. Gmail sometimes returns `Cc: [not present in Gmail response]` on a reply; take the cc from the earlier messages then.
- The RFC `Message-ID` of the message being replied to (for `in_reply_to`).

### 3. Current facts (stale-fact guard)

Map the thread to an engagement: sender domains against `~/Documents/engagements/_aliases.yaml`, else subject or names. Then read, in `~/Documents/engagements/<name>/`:
- `STATUS.md` top 3 to 5 entries, `CONTEXT.md` stakeholders, `COMMERCIAL.md` last entry.
- `atlas/_state/<name>.md` if present.

For every fact, promise, date or "I'll send X" in the intent, check whether it already happened or changed:
- STATUS entries newer than the thread.
- Gmail: `from:me` and `from:<colleague>` on the same topic since the last thread message (someone else may have sent it already).
- Out-of-office replies from recipients: they land in their own thread, so search `("Automatic reply" OR "Automatische Antwort" OR "Out of office" OR "Abwesenheit") newer_than:14d` with the recipients' names. A recipient out until a date breaks any meeting or ask you'd put before it.
- Dates: check the weekday against today's date. "Fri 23 Oct" must be a Friday.

Report what you found in the preview as "Already happened / changed". If STATUS is older than the thread, say so and trust the thread.

### 4. Who is away

Run `python3 ~/Documents/atlas/.claude/scripts/autopilot_common.py away list`. Lines marked `AWAY` are away today, with the cover owner and topic routes. Use it for:
- cc: keep them (hard rule above).
- Opener and owners: never "Hi Jordan," or "Jordan will send". Use the cover for the topic (first name, no @ in email).
- Commercial owner check (hard rule above).

### 5. Recipients

Reply:
- **To** = sender of the last real message, or the person the intent addresses.
- **Cc** = every other participant from step 2, minus Ivo, minus the To.
- Then compare against the people STATUS/CONTEXT say are involved now (for example a new decision maker, or the cover while someone is away). Propose additions as a question, don't add silently.

New email: To and Cc from CONTEXT stakeholders and the intent; show them as a question if not obvious.

Fix `jordan.ryken@` to `jordan_ryken@`. Show every address in full in the preview.

### 6. Attachments and links

- If the intent or the draft mentions a deck, results, document, link or "attached", read `ARTEFACTS.md` (IRIS-produced) and, if relevant, `SOURCES.md` (client-given) and propose up to 3 candidates with where they live (repo path, `drive_id`, or hosted URL + access code).
- Ask in one line: "Attach X (repo path or drive_id)? Or link Y instead?" Never attach silently.
- Body and attachments must agree: no "attached" without an attachment, no attachment the body doesn't mention.
- Local files attach with `{"path": "<abs path>"}`. Drive files: `mcp__gcal__get_drive_file_download_url` then `{"url": ...}`. Drive mount path: memory `drive-sync-mount`.

### 7. Draft

- Follow the voice skills. English to clients: "Hi <first name>," then the purpose in the first sentence. No "I hope this finds you well", no reflexive "sorry", no hedging on facts.
- Default under about 120 words. One concrete ask at the end, with options or a date, when there is an ask.
- Facts only from the thread, the repo or Ivo. A missing fact becomes `[?]` plus a question to Ivo, never a guess.
- Selling-skills lens on client email: structured claim (what, by when, who decides), gap stated as a plan, real versus roadmap kept apart.
- Subject for a reply: `Re: <the original subject as Ivo first sent it>`, without the client's `[EXTERNAL EMAIL]` tag.
- Scan the body and remove: em and en dashes (U+2014, U+2013), arrows (U+2190 to U+21FF), curly quotes (U+2018 to U+201D), the ellipsis glyph (U+2026), bullet glyphs (U+2022), `~` and `**`. Check: `grep -nP '[\x{2013}\x{2014}\x{2018}-\x{201D}\x{2026}\x{2022}\x{2190}-\x{21FF}~]|\*\*'` on the body.

### 8. Preview, then create the draft

Show in chat:

```
To:      ...
Cc:      ...
Subject: Re: ...
Thread:  <thread link>  (reply to <sender>, <date>)
Attach:  none | <file>   (confirmed)

<body>
```

Then a short "Checks" list: already happened or changed (step 3), who is away and how they are handled, guesses marked `[?]`, borderline phrases, and "it's after 18:00 BG, schedule send for 09:30 in the Gmail UI?" when relevant (the API cannot schedule).

- Open questions (attachment, unclear recipient, `[?]`): ask them in one message, wait, then create.
- No open questions: create the draft right away.

Create with `mcp__gcal__draft_gmail_message`:
- `thread_id`, `in_reply_to` = the Message-ID from step 2, `subject`, `to`, `cc` (comma-separated), `body`, `body_format="plain"`.
- `include_signature=false` (the sign-off is already in the body), `quote_original=false`.
- `attachments` only as confirmed in step 6.

Then show the result: "Gmail draft created in thread <subject>. Review: https://mail.google.com/mail/u/0/#drafts (thread: https://mail.google.com/mail/u/0/#all/<thread_id>). Not sent."

### 9. If the Gmail tool fails

Say it loudly at the top, never bury it:

```
GMAIL DRAFT NOT CREATED: <exact error>
```

Then the full draft (headers + body in one copyable block) and the exact fix:
- Auth or scope error: run `mcp__gcal__start_google_auth` (user `ivo@iris.ai`), finish consent in the browser, then say "retry".
- Server missing or tool not found: `claude mcp list`; `gcal` must be connected. It runs from `~/.config/workspace-mcp/run.sh` (`uvx workspace-mcp`). Restart Claude Code after fixing.
- Thread or Message-ID error: retry once with `thread_id` only (no `in_reply_to`) and say you did.

Last resort, not threaded: queue it in the approvals inbox (`http://127.0.0.1:8096`):
`python3 ~/Documents/atlas/.claude/scripts/approval_queue.py add --kind gmail_draft --engagement <name> --title "<subject>" --to "<to>" --cc "<cc>" --subject "<subject>" < body.txt`.
Clicking approve there creates a Gmail draft (new thread, not a reply).

### 10. After

If Ivo edits the draft, offer to save the before and after pair to `~/Documents/digital-twin-ivo/work/edits/` (per `ivo-voice`). STATUS logging of sent client email is done by the Stop hook; don't write STATUS here unless asked.
