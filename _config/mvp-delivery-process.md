# MVP delivery process (agreed 2026-08-11)

How IRIS runs client MVPs across Axion + Neuralith + front end. Agreed on the "Document Extraction MVP Flow" call, 11 Aug 2026.
Attendees: Ivo, Vankata, Petar Ivanov (Axion lead), Borislava/Bobby (Neuralith), Vova (front-end tech lead), Vasil.
Victor absent — Petar flagged twice he had not yet cleared the ownership split with him.

Transcript: Tactiq `mnkXOFEcMzlFhrqyJ7vd`, 53 min.

## Roles

| Who | Owns |
|---|---|
| **Ivo** | Product requirements, business understanding, client relationship, project management. **Not code.** |
| **Axion (Petar's team)** | All backend implementation. Petar, verbatim: "we're taking everything, you should not do anything on the code." |
| **Neuralith front end (Vova, tech lead)** | UI, built as a Neuralith feature (not a standalone app in a branch). Starts early, in parallel, against real backend artifacts. |
| **Vankata** | Arbitrates scope + which team owns what. |

Petar has claimed **all** POCs for himself for now. Rationale given: distributing work was tried for a year and failed (his words: motivation problems, bad knowledge-transfer examples). Plan is to own everything first, then figure out distribution. Bobby challenged this as a bottleneck; Vankata did not overrule it.

## The two structures (these are DIFFERENT — do not merge)

### 1. Technical kickoff — one-off, per MVP

- **Trigger: the data arrives.** Not before.
- **Who:** everyone technical + all tech leads.
- **Ivo's job:** present the overview. What the problem is, the cases, the shape.
- **Their job:** each tech lead states what their team has already built that applies → brainstorm who does what.
- **Purpose:** stop two teams building incompatible implementations of the same thing. Explicitly check whether someone already has a pattern (e.g. a classification agent) before anyone writes new code.

### 2. Weekly working group — recurring, per MVP, starts AFTER kickoff

- **Who:** ONLY people assigned to that MVP. For CMC, Vankata named Petar + Vova.
- **Not Bobby** — Vankata excluded her from the CMC weekly by name.
- **Why tight:** at 10-20 MVPs, if everyone attends everything, Petar and Bobby are in meetings all week.
- **Format:** status only. Who's doing what, how it's progressing. Not planning.
- **Slot:** Tuesday after plannings, or Wednesday. **UNDECIDED — Vankata left it to Ivo.**
- **Internal only** (confirmed in-call).

## Rules

- **No build starts until ALL data has landed.** Vankata: building on one document risks overfitting. Cienby alone develops but does not validate.
- **The clock starts by email, not by signature.** Send "with this data we're now picking up the project, we now track time." SoW signature is NOT the trigger. Term is 8 weeks from that email.
- **Front end starts early**, in parallel with backend, integrated against real artifacts — the lesson from SMS group, where UI work happened after and needed rework.
- **POCs ship as Neuralith features**, living in the Neuralith project. Not separate apps in separate branches.

## Six-month direction

Vankata's target: MVPs become **configuration over reusable components**, not custom code per client. Backend holds agents/systems/processing; a config layer (JSON or similar) sits on top; serving an MVP = defining the config, running it, getting results. Less precise and less bespoke than today, but deliverable with minimal engineering involvement.

Today's state (Petar): the code is mid-migration, "not totally agentic, not totally monolith." End-of-year vision is a PDF-parsing agent + extraction agent you hand a PDF and get text + tables back.

## Open, unresolved

- **Complaint coding ownership: Axion or Neuralith?** Vankata floated Neuralith taking it outright (no parsing, no extraction, just free text). Bobby's objection: if Axion builds a bespoke classification agent now, it won't follow the framework and will never integrate. Vankata deferred it to "let's look at the data." **Decide at that MVP's technical kickoff.**
- **Vankata's framing of classification as ontology:** define labels + descriptions + trigger conditions, agents evaluate them; mutually-exclusive labels need resolution logic. He'd build that as the configurable product surface.
- **App permissions / org scoping** (Vova). Precedent: SMS group sees only their page. Unresolved with the backend team; parked into a separate applications discussion.
- **Victor has not signed off** on the ownership split.
- **Per-value provenance** (Ivo's CMC requirement): raised in-call, never answered. See engagement state.

## Trigger checklist — when client data lands

1. Send the clock-start email → 8 weeks begins.
2. Book the technical kickoff (Ivo presents; Petar, Vova, Bobby, Vankata, Victor).
3. Coming out of kickoff: assign owners, then start the weekly working group with only those people.
4. Front end starts in parallel, against real artifacts.
