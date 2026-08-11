# Scoping Intake — pre-meeting questionnaire

Sent to the client after SQL (first meeting done), before the scoping call. Goal: pull forward the discovery that currently eats 3-4 calls, and make the act of answering surface the client's own data gaps — so they show up to the scoping call already knowing where the holes are.

Built from recurring patterns across 11 engagements (Aumovio, Fresenius x3, Garrett, SMS, Agrolimen, Heineken, T&F, NHS, Daikin). Mom-Test-shaped: asks about **what happens today** and **real artifacts**, not hypotheticals — because the hypothetical answers are the ones that turned out worthless.

---

## How to use this

Fill what you can. Half-answers are useful — a blank tells us where to dig on the call. Attach 5-10 real example documents (the messy ones, not the clean ones). ~20 minutes.

---

### 1. The job done by hand today
- Walk us through the last time someone did this manually, start to finish. Who, which document, what did they type where?
- How long did that one take? How many like it per week/month?
- Who checks their work, and what counts as a mistake when they do?

> Why past-tense, one real instance: it surfaces the tacit rules nobody wrote down. (Aumovio's "48 weeks/year", complaint-coding's when-to-apply logic "in reviewers' heads" — both only appeared this way.)

### 2. The documents themselves
- What formats and languages? (PDF scanned vs digital, Excel, XML, CAD, email…)
- Show us the *most annoying* example you deal with — the one that breaks people or takes longest.
- Are two documents of the "same type" actually laid out the same, or does every source/vendor differ?

### 3. What comes out the other end
- Attach the template, schema, or spreadsheet the answer lands in today. If there isn't one, describe the columns/fields someone fills.
- Which fields matter most — where is a wrong value expensive, and where is it cosmetic?

> The output template is effectively the contract. Every engagement that had one moved faster.

### 4. The rules that aren't in the documents
- Give one example where the right answer needed knowledge that isn't printed on the page (a conversion, a "we always…", a judgment call).
- When two people do this, do they ever disagree on the answer? On what kind of case?

> This is the question clients can't answer in the abstract — it only comes out against a real document. If it's hard to answer, flag it; that's the scoping call's job.

### 5. Scale and the sample
- Sample for the pilot vs. full volume once live? (rough numbers fine)
- Can you share a small set that includes the hard cases, with the correct/expected answers already filled in? The correct answers are what we score against — without them we can't prove accuracy.

> The single most common stall: files arrive, but with no "right answer" attached (complaint-coding), or the hard cases never get curated in time (T&F).

### 6. Getting the data to us
- Who on your side can actually export and send the files? (name a person, not a team)
- Any freeze, migration, or approval that gates the export in the next 4 weeks?
- Cloud or on-prem requirement, and is a security review needed before data moves?

> Also a repeat staller: Aumovio's files sat because only one person had transfer access and he was on holiday. Name the sender now.

### 7. Who decides
- If the pilot works, who signs the budget — and is that the same person we've been talking to?
- Anything triggering the timeline (regulation, project, a system going live)?

---

## For internal use — how this maps to the 2-call flow

- **Call 1 (SQL / Jordan):** qualify + send this form + issue the upload link. Ends here.
- **Client fills form + uploads sample (async).** The form does the interviewing; the playground/first extraction does the gap-finding Brian used to do live.
- **Call 2 (scoping, technical):** starts from filled form + first-pass extraction on their real docs. No re-asking §1-6. Call is spent on the §4 rules and §3 edge fields — the stuff that genuinely needs dialogue.

Sections 1 and 4 are the Mom Test core: they can't be answered well from a desk, so a weak answer is itself the signal for where the call goes. Everything else (2, 3, 5, 6, 7) is factual front-loading that today wastes call time.
