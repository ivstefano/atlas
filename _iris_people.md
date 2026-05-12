---
name: iris-people
description: "IRIS.ai people — names, nicknames, roles. For decoding Tactiq transcripts (which mislabel speakers) and writing engagement docs."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 097b7a4b-6b20-42d8-b183-53ecdf288975
---

IRIS.ai team — name ↔ nickname ↔ role. Tactiq transcripts frequently mislabel these speakers (e.g. "ivan_tsenov", garbled spellings), so use this to disambiguate when writing engagement context.

- **Ivaylo Stefanov** = "Ivo", "I" — solutions architect; runs the engagements (the user; "Ivo" throughout the docs).
- **Ivan Tsenov** = "Vankata" — engineer / tech lead on PoCs; the technical voice on client calls.
- **Borislava** = "Bobi", "Bobby" — engineer; does PoC builds (e.g. assigned to the Heineken PoC).
- **Martina** = "Marti".
- **Viktor** — CTO.
- **Jordan Ryken** — Principal Sales Director; runs client accounts, books calls, drives commercial conversations.
- **Steven** — CRO. (The ENGAGEMENT_PLAN's "CFO brief for Steven" wording in §6 step 9 mismatches this — he's CRO; treat that line's "CFO" loosely or fix it.)

Client-side names live in each engagement's `CONTEXT.md` §6 (e.g. Heineken: Justyna Roczek = Justyna Bień, married — both surnames appear in transcripts; Lucy Todorovska; Monika Samolej).

Related: [[heineken-engagement]] (if written), the `engagements/` repo, [[atlas-state]] (if written).
