---
name: iris-people
description: "IRIS.ai people — names, nicknames, roles. For decoding Tactiq transcripts (which mislabel speakers) and writing engagement docs."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 097b7a4b-6b20-42d8-b183-53ecdf288975
---

IRIS.ai team — name ↔ nickname ↔ role. Tactiq transcripts frequently mangle these speaker labels ("ivan_tsenov", "Vankata Tsenov", "Wanka", "Banga", garbled spellings), so use this to disambiguate when writing engagement context.

- **Ivaylo Stefanov** = "Ivo", "I" — solutions architect; runs the engagements (the user; "Ivo" throughout the docs).
- **Ivan Tsenov** = "Vankata" (also "Venkata", "Vanka", "Wanka", garbles) — **CPO**. The senior technical voice on client calls (what the platform does, what "next" looks like, managed-service framing); joins for the deep technical questions. *In EVERY transcript "Vankata"/"Vankita" = Ivan Tsenov, IRIS CPO* — even when an engagement's notes seem to imply a client-side "Vankata" (e.g. an earlier draft of the Garrett docs wrongly invented a "Garrett CPO Vankata"; there is no such person — "the CPO will join" meant IRIS's CPO joining IRIS's side).
- **Borislava** = "Bobi", "Bobby" — engineer; does PoC builds (e.g. assigned to the Heineken PoC).
- **Martina** = "Marti".
- **"Matyo"** — ML scientist (IRIS side); ran the Chandra-2 / DocLayout-YOLO / GPT-4o-vision extraction work on Garrett.
- **Viktor Botev** (also "Victor Botev") — CTO. NDA signatory on some client contracts.
- **Jordan Ryken** — Principal Sales Director; runs client accounts, books calls, drives commercial conversations.
- **Steven** (Steven Fung) — CRO. (The ENGAGEMENT_PLAN's "CFO brief for Steven" wording in §6 step 9 mismatches this — he's CRO; treat that line's "CFO" loosely or fix it.)
- **Michael Sica-Lieber** — sourced/handled some leads (lemlist outbound); Ivo took over aumovio and agrolimen from him ~Mar 2026.
- Engineers seen on specific PoC builds (not exhaustive): **Petar Ivanov** (petar@iris.ai — aumovio early PoC, sms-group), **Martin Kondov** (aumovio build V2→V7), **William Le Roux** (sms-group original technical owner), **Aleksandar Georgiev** (sms-group build / demo).

Client-side names live in each engagement's `CONTEXT.md` §6 (e.g. Heineken: Justyna Roczek = Justyna Bień, married — both surnames appear in transcripts; Lucy Todorovska; Monika Samolej).

Related: the `engagements/` repo, `atlas/STATE.md` (the durable handoff doc — has a per-engagement rundown), `atlas/_iris_people.md` (a working mirror of this file the subagents read), `atlas/_migration_protocol.md` (the reusable engagement-migration procedure).
