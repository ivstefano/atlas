---
description: End-of-tab wrap. Save STATE, file client work into the engagement, commit+push only this session's files, retire worktree, say if safe to close.
argument-hint: "" | dry (report only, change nothing)
---

# Wrap this tab

Replaces "save status, commit, push, can I close this tab". Run the steps in order, no
questions unless a step says ask. Argument: `$ARGUMENTS` (`dry` = run step 0 and print the
plan for 1-5, change nothing).

## 0. Inventory (read-only)

```
python3 ~/Documents/atlas/.claude/scripts/wrap.py
```

Prints: task, worktree (if any), per repo the files this session edited (Edit/Write tool
calls in this session + its subagents) with git state, "dirty, not confirmed" candidates
(dirty, changed during the session, but not via Edit/Write: Bash-written, autopilot, or
someone else's), engagement files missing from ARTEFACTS.md, and this week's meta-work
hours vs cap. `--json` for structured output. Add to the confirmed list anything you know
you wrote via Bash this session (cp, mv, scripts, renders) from your own context.

## 1. Checkpoint STATE

Same as `/state save`: update `~/Documents/atlas/_state/<task>.md` from this conversation
(keep `## Now` / `## Next action` / `## Open threads` / `## Don't re-explain`, set
`last_session` to now), then rebuild the board:
`python3 -c "import sys; sys.path.insert(0,'$HOME/Documents/atlas/.claude/scripts'); import state_flush; state_flush.refresh_index()"`.
STATE always lives in the main atlas checkout, even from a worktree. Never invent facts.

## 2. File client work

For anything produced for a client this session (drafts, decks, docs, demo files, renders):
- It lives under `~/Documents/engagements/<client>/` in the right stage subfolder
  (`1_pre-scoping/`, `_briefs/`, etc., follow what that engagement already uses). If it was
  written to /tmp, a scratchpad or atlas, move it there. Demo files under
  `engagements/_demo-builder/demos/<client-demo>/` stay put but still get listed in the
  client's ARTEFACTS.md.
- Add one entry to that engagement's `ARTEFACTS.md` (IRIS-produced; client-given goes to
  `SOURCES.md`). Use `repo:` / `drive:` + `drive_id` prefixes, say sent vs drafted, date.
  `NOT-IN-ARTEFACTS` in step 0 marks the gaps.
- Client unclear: ask (one question, options = likely engagements).

## 3. Commit and push only this session's files

Per repo from step 0, commit ONLY confirmed session files (plus the STATE/INDEX and
ARTEFACTS edits from steps 1-2). Never `git add -A`, never `git commit -a`.

```
git -C <repo> add -- <paths>
git -C <repo> commit -m "<one plain sentence of what was done>" -- <paths>
git -C <repo> push origin <branch>
```

- "Dirty, not confirmed" files: leave alone unless you know this session wrote them; if
  unsure, list them and ask once.
- Gitignored files (git=ignored) are not committed; mention them only if they matter.
- Message: one natural sentence, no AI attribution, no Co-Authored-By.
- atlas pushes `origin main` (GitHub). engagements pushes `origin master` (Bitbucket).
- Push rejected: `git -C <repo> pull --rebase --autostash origin <branch>` then push again.
  Conflict: stop, `git rebase --abort`, report it as a blocker.
- `unpushed` > 0 before your commit means older local commits exist; pushing ships them
  too. Fine for Ivo's own repos, but name them in the report.

## 4. Worktree

If step 0 printed `WORKTREE`, do the finish-and-retire flow (memory
feedback_worktree-workflow.md), as one go:
1. commit pending session work on the worktree branch
2. in the main repo: `git merge --no-ff <branch>` (main repo must not have conflicting
   uncommitted changes in the same files; if it does, ask)
3. rsync gitignored data the worktree produced into the main checkout
4. push main branch, and `git push origin <branch>` as archive
5. `git worktree remove --force <path>` + `git worktree prune`
6. `git branch -d <branch>` (`-D` if needed)

Skip and ask if the worktree belongs to another running agent (`locked` in
`git worktree list` and not this session's cwd), or the merge conflicts. Removing the
worktree you are standing in kills the cwd: do it last, from the main repo path.

## 5. Report (3-5 lines, then verdict)

```
Next: <next action, from STATE>
Open: <1-3 open threads>
Committed: <repo: short sha, N files> ...  Pushed: yes/no
Meta-work: <X h / cap h this week>  (add "over cap" if over)
SAFE TO CLOSE   |   NOT SAFE: <what blocks>
```

Not safe when any of: session files still uncommitted or unpushed, a "dirty, not
confirmed" question unanswered, a background job from this session still running, push or
merge failed, client file not filed or not in ARTEFACTS.md.

## Meta-work cap

Cap: `meta_cap_hours_week` in `~/Documents/atlas/_autopilot/config.json` (default 5 if
absent; accessor `autopilot_common.meta_cap_hours()`). Heuristic in the `wrap.py`
docstring: a session counts as meta when its cwd is a tooling repo (Cognion, capabilities,
digital-twin-ivo) or at least half its edits land in atlas/.claude, _autopilot, _config,
~/.claude, ~/.config. Active time = message gaps capped at 5 min. Breakdown:
`python3 ~/Documents/atlas/.claude/scripts/wrap.py meta -v`. Report only, no blocking.
