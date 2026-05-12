# Post-meeting digest protocol (retroactive — fold Drive Gemini-notes into an engagement folder)

You are updating ONE engagement's `engagements/<company>/` files from meeting content that lives in
Google Drive as "Notes by Gemini" docs (and sometimes "Transcript" docs) that weren't migrated.
This is the LOOPS.md #2 "post-meeting digest" run retroactively.

## Tools you'll use
- `mcp__claude_ai_Google_Drive__read_file_content` — pass the Drive `fileId` (given to you), get the
  natural-language text of the doc. (For Google Docs it just works; no exportMimeType needed.)
- `mcp__claude_ai_Google_Drive__search_files` — if a doc you need isn't in the IDs given, search:
  `title contains '<company>'` or `fullText contains '<keyword>'`.
- Read/Edit/Write on the local `engagements/<company>/` files.

## What to do
1. Read the current `engagements/<company>/{CONTEXT,STATUS,SOURCES}.md` (and `COMMERCIAL.md` if relevant).
2. For each Drive doc ID given to you: `read_file_content`, digest it.
3. **Update `STATUS.md`** — add or correct one entry per meeting (newest on top, ABSOLUTE dates).
   If an entry for that date already exists (from the original migration), enrich/correct it rather
   than duplicating. Each entry: What happened / Stage / Blocked on / Next action (owner, by-date) /
   Notes (cite the Drive doc, e.g. "Source: Drive Gemini notes `<title>` (fileId <id>)").
4. **Update `CONTEXT.md`** where the picture changed — especially: the open questions the migration
   flagged (resolve them if the notes answer them), stakeholders (new names/roles), §4 "what they
   care about", §5 data, §7 current phase. Keep Heineken's voice. Don't rewrite wholesale; surgically
   update.
5. **Update `SOURCES.md`** — under "Meeting notes / transcripts", add lines for the Drive Gemini-notes
   docs: `Drive (Gemini notes): "<title>" — <one-line what-it-covers> — fileId <id>`. (These stay in
   Drive; we reference them, like the AXION: paths.)
6. **Do NOT git commit.** The parent does one commit. Don't `cp` anything — these stay in Drive.
7. Report back: a 1-paragraph summary of what changed, which open questions you closed, anything
   surprising, anything still unknown.

Voice in CONTEXT.md: descriptive, factual, like the Heineken one. STATUS/SOURCES looser is fine.
If a Gemini-notes doc turns out to be about a *different* engagement than expected, say so and skip it.
