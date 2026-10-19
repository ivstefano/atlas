---
description: Draft Ivo's Slack reply to a real thread, in his voice and the thread's language, short, with an explicit ask and no pings to people who are away. Never posts.
argument-hint: <Slack thread URL | channel ts> [what Ivo wants to say] [queue]
---

# /reply

Draft what Ivo can say in a Slack thread. Input: `$ARGUMENTS` = a Slack URL (or `<channel> <ts>`), optionally Ivo's take ("say we can do X by Thu"), optionally `queue`.

The output is a draft in chat in a copyable block. Nothing is posted.

Why this command exists: Ivo pasted Slack threads asking "what can I say" 55 times. Drafts went wrong because the voice skill wasn't applied (he had to ask, plus 26 reminders), they were too long, they answered the wrong person or pinged someone on PTO, the tone was off, the language was wrong (Bulgarian), or the ask was unclear.

## Hard rules

- Never call a Slack write tool. Posting happens only by Ivo, or by his click in the approvals inbox (`queue`).
- Never @mention anyone marked away (step 4). Route to the cover.
- Reply in the language of the message being answered.
- Facts only from the thread, the repo or Ivo's take. A missing fact becomes `[?]` plus a question to Ivo.
- No em or en dashes, arrows, fancy quotes, bold headers. No reflexive "sorry". No hedging on facts.

## Steps

### 0. Load the voice first (non-negotiable)

Invoke the `ivo-voice` skill (Slack row: `voice_written.json` + `backtest/twin_prompt.md`) before anything else, then `human-writing`. Do this every run, without being asked. If the twin files can't be read, say so at the top of the answer.

### 1. Resolve the thread

- URL `https://irisai.slack.com/archives/<C>/p<digits>[?thread_ts=<parent>]`: channel = `<C>`; ts = `<digits>` with a dot before the last 6 (`p1792404554330179` is `1792404554.330179`). Use `thread_ts` from the query string as the parent when present, else the message ts (the API accepts any message in the thread).
- `<channel> <ts>`: use as given (channel id, `#name` or `@user_dm`).
- Pasted text with no URL: find it with `mcp__slack__conversations_search_messages` (a distinctive phrase, `filter_date_after` a few days back). If not found, work from the paste and say the thread wasn't read.

Read it with `mcp__slack__conversations_replies(channel_id, thread_ts, limit="200")`. Resolve `<@U...>` ids with `mcp__slack__users_search` when the name isn't in the rows.

### 2. Who asked what

Before drafting, list for yourself every open question or request in the thread: who asked, of whom, and whether someone already answered it later in the thread. Then pick what Ivo is replying to:
- Ivo's take names it: use that.
- Else the latest unanswered item aimed at Ivo (by @ or by name), else at the group in a channel where Ivo owns the topic.
- Two or more plausible targets, or the latest message is from someone other than the person Ivo should answer: ask Ivo which one, with 2 or 3 options ("(A) Ivan's ask for a feature breakdown, (B) Jordan's point on loan decisioning, (C) both in one reply"). Never answer the wrong person.

If the thread already answered the question (someone else replied, or the matter moved), say so instead of drafting: "Steven already answered this at 10:39, nothing needed from you", with an optional reaction suggestion.

### 3. Context and current facts

Map the thread to an engagement (channel name, client name in the parent, `~/Documents/engagements/_aliases.yaml`). Read `STATUS.md` top 3 entries and `atlas/_state/<name>.md` if present. Use them to check facts in the draft, and flag when STATUS is older than the thread. Keep the reply to what the thread is about; don't import unrelated engagement detail.

### 4. Who is away

Run `python3 ~/Documents/atlas/.claude/scripts/autopilot_common.py away list`. For each `AWAY` person:
- No @mention, no "cc @<name>", no opener addressed to him, no next step owned by him, even when he wrote in the thread.
- Things that would go to him go to the cover: match the topic against the cover routes (first route whose words fit), else the default cover. @mention the cover.
- If he asked something in the thread, answer the content without the @, or hand it to the cover ("@Eric can you take the AWS form while Jordan is out?").

### 5. Language

Reply in the language of the message being answered. Bulgarian to Bulgarian speakers (Vankata, Yovcho, Vladi, Matyo, Aleks, Ivan G.) when they wrote in Bulgarian, with English tech terms kept as is; casual register, the vocative of the name. English whenever the thread is English or anyone in it doesn't speak Bulgarian (clients, Jordan, Steven, Eric).

### 6. Draft

- Default 1 to 3 short lines (his median is about 12 words; threads about 16). Go longer only for a plan check, status or feedback, and then under about 150 words, plain labels, no bold.
- A request gets an explicit ask: what, who, by when. "Can you send the system list by Wed 21 Oct, @Steven?" A decision gets the recommendation first: "Recommendation: X. Need from you: Y by Z."
- Pushback stays a plain statement with the reason, not a softened question.
- Capital letter at the start of each sentence in work threads (lowercase is fine only in Bulgarian DMs to close colleagues).
- One message. If the answer has two parts, two short paragraphs in the same message, not a burst.
- Before showing it, run the typography check from `/email` step 7 on the draft (no dashes, arrows, curly quotes, ellipsis or bullet glyphs).
- Use his real phrases sparingly ("Got it", "I'll check and let you know", "what can I prepare?"). No stock emoji on a factual reply.

### 7. Output

```
Replying to: <Name>, <their point in a few words> (<time>)
Language: EN | BG    Away: <names, how handled> | none
```

Then the draft in a fenced block, ready to copy. Write mentions as `@First`; tell Ivo that pasted `@First` text is not a live mention, he retypes the @ in Slack (the `queue` path converts known names automatically).

Then at most 3 check lines: guesses marked `[?]`, a borderline phrase, "it's after 18:00 BG or weekend: schedule send for 09:30?".

Offer one alternative only when the tone call is close (for example firmer versus warmer), each still 1 to 3 lines.

### 8. Queue to the approvals inbox (optional)

When `$ARGUMENTS` contains `queue`, or Ivo says "queue it" after seeing the draft:

```bash
python3 ~/Documents/atlas/.claude/scripts/approval_queue.py add \
  --kind slack_thread_reply --engagement <name|operations> \
  --title "Reply to <Name> in #<channel>: <topic>" \
  --channel <C...> --thread-ts <parent ts> --permalink "<url>" <<'EOF'
<draft text>
EOF
```

It prints the item id. The draft then waits at `http://127.0.0.1:8096`; it posts only when Ivo clicks "Approve & reply in thread", and `@Jordan`, `@Steven`, `@Eric`, `@Vankata`, `@Ivan Tsenov`, `@Ivan Georgiev`, `@Vasil` become real mentions there. Other names stay plain text.

### 9. After

If Ivo edits the draft, offer to save the before and after pair to `~/Documents/digital-twin-ivo/work/edits/` (per `ivo-voice`).
