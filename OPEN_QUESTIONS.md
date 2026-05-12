# Open questions and logged decisions

## Decisions made (logged 2026-05-12)

- **Prototype set for Layer 1**: Heineken, Aumovio, SMS. ✔
- **Slack**: needs a live Slack MCP connection (not paste-in `SLACK.md` exports). Action item
  to find/stand up a Slack MCP server — see `MCP_SETUP.md`. ✔
- **Loops**: local `/loop` first; iteratively work out what to outsource to cloud `/schedule`
  remote agents. ✔
- **Auto-drafting**: nothing is forbidden from being drafted, BUT contract-grade docs (SoW,
  NDA) must be generated and reviewed with me in the loop — they don't leave / aren't final
  without my review. ✔
- **First deliverable**: a written plan in `_optimize/` (this folder) before any scaffolding. ✔
- **Mobile-in-the-loop approval is in scope** (new Layer 4): approve/edit/reject Claude
  sessions from a phone, decoupling the person from the desk; applies to me and to Victor /
  Vankata / Steven on the tech side. The gate is action-classified (auto-run / notify-me /
  needs-my-approval / needs-escalation), not a blanket approve button; high-tier actions never
  auto-proceed on a timeout. See `MOBILE_APPROVAL.md`. ✔

## Still open

1. **Filenames for Layer 1 files.** `CONTEXT.md` collides with the existing RAG-grounding file
   at `scoping/heineken/human-in-the-loop/CONTEXT.md`. Pick one:
   - `ENGAGEMENT.md` / `STATUS.md` / `SOURCES.md` (no collision), or
   - keep `CONTEXT.md` and rename the RAG one (e.g. `KNOWLEDGE_BASE.md`), or
   - namespace the engagement files under `_meta/` in each folder.
2. **Generate vs. hand-maintain Layer 1 initially.** Script/agent that builds `CONTEXT.md`/
   `STATUS.md`/`SOURCES.md` from existing folder contents, or write the first three by hand and
   automate later?
3. **Slack MCP choice.** Official/community server with a bot token, or self-hosted? Which
   channels in scope? Post-as-me vs. post-as-bot?
4. **Where loop outputs live.** `_optimize/briefs/`, `_optimize/rollups/` inside this repo, or
   somewhere else (Drive)? Commit them to git or keep untracked?
5. **"Active" definition for the stale-engagement watchdog.** What phases count as active, and
   what's N (days untouched before a flag)?
6. **Judge-agent scope.** Does the second "LLM judge" check only SoW/NDA drafts, or also weekly
   client updates and the rollup?
7. **Mobile approval mechanism.** Claude Code native push (`PushNotification` / `RemoteTrigger`)
   vs. Slack-as-approval-channel vs. cloud remote-agent UX vs. email. Leaning Slack-as-channel
   first (reuses the Slack MCP, everyone's on mobile Slack) + evaluate native push in parallel.
8. **Per-person approver mapping.** Confirm: I approve engagement/commercial actions; Victor /
   Vankata / Steven each approve their own tech-side loops; cross-approval only where it makes
   sense. Any exceptions?
9. **Timeout behavior.** Confirm default for needs-my-approval and higher is "wait, do not act,
   send a reminder" — never escalate-by-default (the codex-pinged-the-manager failure mode).
