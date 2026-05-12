# Gmail digest protocol (enrich an engagement folder from email threads)

You are enriching ONE engagement's `engagements/<company>/` files from Gmail threads — the
back-and-forth between calls, data-handoff logistics, the pre-Jordan / proposal threads, the
"going cold" signals. Same spirit as `_digest_protocol.md` but the source is email.

## Tools
- `mcp__claude_ai_Gmail__search_threads` — query with Gmail syntax (`from:`, `to:`, `subject:`, `newer_than:`, `OR`, etc.). Returns thread IDs + message snippets/headers (NOT full bodies).
- `mcp__claude_ai_Gmail__get_thread` — pass a `threadId`, `messageFormat: FULL_CONTENT`, get the full message bodies. Use this on the threads that look substantive.
- Read/Edit/Write on the local `engagements/<company>/` files.

## What to do
1. Read the current `engagements/<company>/{CONTEXT,STATUS,SOURCES,COMMERCIAL}.md`.
2. Search Gmail for the engagement (you'll be given starting queries). **Skip the noise** — pure
   calendar-invite accept/decline/reschedule emails, HubSpot/Tactiq notifications, auto-replies,
   "X sent a message" Teams notifications carry almost nothing; don't `get_thread` those unless the
   snippet shows real content. **`get_thread` only the threads with actual substance** (proposals,
   data-handoff logistics, scope clarification, redlines, "we're delayed because X", new-stakeholder
   intros, anything that changes the picture).
3. **Update `STATUS.md`** — add/correct entries (newest on top, ABSOLUTE dates). If an entry for a
   date exists, enrich rather than duplicate. Cite the email (subject + date + "Gmail thread"). Email
   captures a lot of scheduling churn — you can summarise "several reschedules Apr-May, blocker = X"
   in one line rather than one entry per bounce.
4. **Update `CONTEXT.md`** where the picture changed — stakeholders (new names + titles — email
   signatures often give the exact title the docs lack), §4 "what they care about", §5 data/access
   status, §7 phase. Surgical edits, keep Heineken's voice.
5. **Update `COMMERCIAL.md`** — proposal threads, pricing back-and-forth, NDA/SoW status, the
   commercial origin story, deal-stage.
6. **Update `SOURCES.md`** — under "Meeting notes / transcripts" or "External", note the key email
   threads (subject + date + thread ID) and any artifacts referenced (a proposal Google Doc link, a
   MoveIT/SharePoint location, a credentials archive — DO NOT paste credentials/passwords; just note
   "credentials sent via encrypted zip, password in a separate email" — never copy a password into
   the repo).
7. **Do NOT git commit.** The parent does one commit. Don't `cp` anything — email stays in Gmail.
8. Report back: 1-paragraph summary of what changed, open questions closed, new stakeholders/titles
   found, anything surprising, anything still unknown.

Security: never write a password, credential, token, or secret into the repo files — note its
existence and where it was sent, nothing more. The `.gitignore` would catch `*credentials*`/`*token*`
filenames but it won't catch a password pasted into a markdown file — so just don't.
