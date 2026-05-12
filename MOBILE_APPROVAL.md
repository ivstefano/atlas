# Layer 4 — Mobile-in-the-loop approval

Decouple the person from the desk. Claude sessions (loops, drafts, agent actions) pause at
their decision points and reach me on my phone: a notification with the context and the ask,
and I approve / edit / reject from there. Same for Victor, Vankata, Steven on the tech side.

## Why this is its own layer (Cherny)

- "The doing of things is now easy; *is this a good thing, is this what I wanted* is the single
  most important bottleneck. Human attention is the scarce resource." So the system has to
  bring the decision *to* the human, not require the human to come to a laptop.
- "Clicking approve, approve, approve is kind of where we've been — and humans are not very
  good at that either." So the gate is not a blanket approve button. The agent classifies each
  action and only the ones that actually need a human reach a human.
- The anecdote: codex pinged a colleague on Slack for help, decided two minutes was too long,
  and escalated to that colleague's *manager*. Reasonable-ish, but should have checked first.
  The fix is not "never let it act" — it's "this class of action needs my OK; surface it to me;
  I'm on my phone."
- Victor, Vankata, Steven (and me) are mobile a lot. A loop or remote agent that can only be
  approved at a laptop is, in practice, an unsupervised loop. Phone approval is what makes
  Layer 3 loops and (later) cloud `/schedule` agents actually safe to run.

## What the agent does (action classification)

Every action a loop/agent wants to take is tagged into one of four buckets, and the bucket
decides who sees it:

| Bucket | Examples | Behavior |
|---|---|---|
| **auto-run** | read a Drive doc, summarize a transcript, update `STATUS.md`, generate a draft into a `drafts/` dir | just do it; log it |
| **notify-me** | "morning brief is ready", "post-meeting digest written for <client>", "stale-engagement flag raised" | push a notification, no approval needed; I can look or not |
| **needs-my-approval** | send a Slack message to a colleague, push a doc to a shared Drive folder, send an email, anything client-facing | pause; phone notification with the full draft + context; I approve / edit / reject |
| **needs-escalation / contract-grade** | SoW, NDA, anything contract-grade; or the agent is unsure which bucket something is in | pause; phone notification flagged high-priority; mandatory human review (me); never proceeds on a timeout |

Key rule, from the codex anecdote: **a "needs-my-approval" or higher action never proceeds on a
timeout.** If I don't respond, it waits. It does not escalate-by-default. (It may send me a
reminder; it does not act.)

## What I do (from the phone)

- See: the notification, the action being requested, the relevant engagement context
  (`CONTEXT.md` summary + recent `STATUS.md`), and the full draft if there is one.
- Do one of: **approve** (proceed as drafted), **edit** (send back a correction, agent revises
  and re-asks), **reject** (don't do it; optionally say why so the agent learns the boundary).
- For "notify-me" items: just acknowledge, or ignore.

## Mechanisms to evaluate

Need to pick how the notification + approve path actually works. Candidates:

1. **Claude Code's own push/notification path** — there's a `PushNotification` capability in
   this environment and a `RemoteTrigger`; check whether a session can push a notification to
   a phone and accept a reply that resumes it. This is the cleanest if it works.
2. **Slack as the approval channel** — once the Slack MCP is wired (see `MCP_SETUP.md`), the
   agent DMs me the ask; I reply `approve` / `edit: ...` / `reject` in Slack; the loop reads my
   reply and continues. Works on Slack mobile, which everyone already has. Good fallback.
3. **Cloud `/schedule` remote-agent approvals** — when loops graduate to cloud, see what
   approval UX the remote-agent product gives (mobile web, app); cloud agents make Layer 4
   mandatory anyway.
4. **Email (Gmail MCP)** — lowest-tech: agent emails the ask, I reply, agent parses. Use only
   if 1–3 don't pan out.

Decision deferred to `OPEN_QUESTIONS.md`. Probably: start with Slack-as-approval-channel
(reuses the Slack MCP work, everyone's on mobile Slack), evaluate Claude Code's native push
in parallel.

## Rollout

- Me first: morning brief "notify-me", post-meeting digest "notify-me", any Slack/Drive/email
  send as "needs-my-approval", SoW/NDA as "needs-escalation".
- Then Victor / Vankata / Steven: same model for the tech-side loops they run (e.g. an extractor
  eval loop, a build/deploy loop). Each of them is the approver for their own sessions; I'm the
  approver for engagement/commercial ones. Cross-approval (e.g. me approving something Vankata's
  loop wants to do) only where it makes sense.
- Tune the buckets over time. Cherny: "we're still building up the EQ of the model." Start
  conservative (more things in needs-my-approval), relax as it earns trust.

## Open items (see OPEN_QUESTIONS.md)

- Which mechanism: Claude Code native push vs. Slack-as-channel vs. remote-agent UX vs. email.
- Per-person approver mapping (who approves what).
- Default timeout behavior is "wait, don't act" — confirm that's right for every bucket.
