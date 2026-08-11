---
description: Client data has landed for an MVP. Runs the agreed delivery process: clock-start email, technical kickoff, then the weekly working group.
argument-hint: cmc | complaint-coding | <engagement name>
---

# MVP kickoff

The client data for an MVP has arrived. This runs the delivery process agreed on the 11 Aug 2026 "Document Extraction MVP Flow" call, so nothing is missed and the 8-week clock starts correctly.

Argument: `$ARGUMENTS` (which MVP; ask if not given)

## Read first (don't reinvent)

- `atlas/_config/mvp-delivery-process.md` — the agreed process: roles, the two structures, the rules, open questions.
- `atlas/_state/fresenius-cmc.md` or `atlas/_state/fresenius-complaint-coding.md` — that MVP's live state.

## Before anything: verify the gate actually opened

Do NOT start the process on partial data. Vankata's rule: building on one document risks overfitting.

- **CMC:** all three products present (Cienby + the two others), inputs AND filed outputs. Cienby alone is NOT enough.
- **Complaint coding:** Brian has confirmed the compiled ground-truth lists.

If the data is incomplete, say so and stop. Report exactly what's missing and who owes it.

## Then, in order

### 1. Clock-start email

The 8 weeks starts from this email, NOT from SoW signature. Draft it, don't send (see the outward-facing rule below).

- To the client owner, cc the same group as the last thread on that engagement.
- Substance: we have the data, we are now picking up the project, we are now tracking time. State the 8 weeks explicitly.
- Check the state file for who's currently out of office before choosing the recipient.

### 2. Book the technical kickoff

One-off, triggered by data. Attendees: Ivo presents, plus Petar (Axion), Vova (front end), Bobby (Neuralith), Vankata, Victor.

Ivo's job is the overview: what the problem is, the cases, the shape. Each tech lead then states what their team has already built that applies.

Draft the invite; Ivo approves before it's created.

**Raise at kickoff, per MVP:**
- **CMC — per-value provenance.** Does the Axion extraction/reconstruction path carry per-value provenance (read-from-source with page click-through, declared-by-us, computed, gap), or only flat text and tables? The client reviewer corrects our judgement calls, so this must be in the backend artifacts from day one or the front end can't show it. Unanswered since 11 Aug.
- **Complaint coding — who owns it, Axion or Neuralith?** Deliberately deferred to "let's look at the data." Vankata floated Neuralith (no parsing, just free text); Bobby warned a bespoke Axion classification agent won't follow the framework and will never integrate. Force the decision here.
- **Both:** does either team already have a pattern for this (e.g. a classification agent)? Check before anyone writes new code.

### 3. Assign owners, then start the weekly working group

Only the people actually assigned to that MVP. For CMC, Vankata named Petar + Vova. **Bobby is explicitly not on the CMC weekly.**

Status only, not planning. Internal.

Slot: Tuesday after plannings or Wednesday — **if Ivo still hasn't picked one, ask him now.**

### 4. Front end starts in parallel

Vova starts against real backend artifacts, not after the backend finishes. This is the SMS group lesson: UI built afterwards needed rework.

## Rules

- **Never auto-send email or create calendar invites.** Draft → Ivo approves → then create.
- Ivo owns requirements and the client. Axion owns all backend code. Vova owns front end. Don't offer to write implementation code.
- After running this, update the MVP's `_state/` file: what was sent, what was booked, what got decided at kickoff.
