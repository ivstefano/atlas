# Platform Onboarding Flow

How I picture onboarding happening on the platform, as far upstream as possible. The client self-serves the setup and the data upload; a human only enters once there's real data to react to.

Built on the recurring intake questions across 25+ engagements. The design principle: get the client to commit data with almost no friction, then ask the real questions once they've uploaded and have their own data fresh in mind. Two passes.

- Pass 1 is deliberately tiny: use case + sample + upload. The goal is to remove every reason not to upload.
- Pass 2 opens right after upload, same session. This is where the questions live: the factual ones we always need, and the detailed ones about how the work is done today that recur across most engagements. In the future they can be customized by AI based on the shared data. They land better here because the client just looked at their own files.

---

## The flow

```
1. Sign up          client creates an account
2. (Playground)     optional: try it on sample/public data first
3. Create Project   name the work + one line on the use case
4. Pass 1 form      use case + sample + upload  (minimal, gates nothing else)
5. Pass 2 form      opens right after upload: factual + detailed questions
   =============== handoff ===============
6. SA takes over    first-pass extraction on their real docs
```

Steps 1-6 are self-serve, no IRIS human required. Step 6 is where we come in, already holding data and answered questions instead of asking about them on a call.

---

## Step 3: Create Project

Minimal. Just enough to name the work and route it.

- Project name
- Your company
- One line: what are you trying to get out of these documents? (free text)

## Step 4: Pass 1 form (use case + sample + upload)

The whole point is low friction. Three things, then the upload button.

- What's the use case, in a sentence or two? (what job should this do for you)
- Upload the template/spreadsheet you fill by hand today, if you have one (file field, optional)
- Upload your sample documents

Nothing here gates the upload with a wall of questions. Everything else waits for Pass 2.

## Step 5: Upload

An upload form, tied to this project so files land in the right place. Replaces the manual link-issuing that today stalls when the link is broken, rejects a format, or only one person has access. Files + Pass 1 answers land together, tagged to the project.

## Step 6: Pass 2 form (opens right after upload)

Now the client has uploaded and their data is fresh in mind. This is where we ask what we always end up asking. Two groups: the quick factual questions, and the deeper questions about how the work is done today and specific real cases (asked about concrete past instances, not hypotheticals, because the hypothetical answers turned out worthless across engagements).

### Factual (things the files don't tell us)
- Are there various languages in the documents, not only English
- Roughly how many document types: structured/unstructured? (one standard form, or every source looks different?)
- How many documents per month once this is running for real? (the upload gives us the first-batch count; this is production scale)
- Cloud or on-prem requirement, and is a security review needed before data moves?
- Who on their side owns providing us the data? (name + email, so we're not blocked on one absent data/person)


### Detailed questions (about the real job, not the ideal one)
- Walk us through the last time someone did this by hand: which document, what did they type where, how long did it take?
- Look at one document you just uploaded. What's the right answer for it, and did getting that answer need anything not printed on the page? (a conversion, a "we always...", a judgment call)
- When two of your people do this, where do they disagree? On what kind of case?
- Who checks the work today, and what counts as a mistake when they do?
- For your uploaded sample: is the correct/expected answer filled in anywhere? (yes / partly / no) This is what we measure accuracy against.
- If the pilot works, who owns the budget, same person filling this in or someone else? (ask for name + email)

> These questions are the ones that stall scoping when asked out of the blue. Combining them with the uploaded files is what makes them answerable: they discover their own gaps while filling this in, instead of us discovering them three calls later. This is what happened with Brian at Fresenius, Phil at Aumovio, Sathya at CMC etc.: none could answer until they saw their data. The form makes that moment happen on their own screen or at least gives an initial boost of the SME thinking in the direction of understanding the data.

---

## Why this works

Today we discover verbally across 3-4 calls what the platform can capture in two forms wrapped around an upload.

- The client commits data as part of onboarding, not after weeks of weeklies. Pass 1 is small enough that there's no reason to stall.
- Splitting into two passes is what makes it work: a big form before upload kills the upload; the same questions after upload get answered, because the data is in front of them and they've made the effort.
- The detailed questions surface the client's own gaps while they fill the form, so they arrive at the first human call already knowing where the holes are.
- By the time we step in, we hold the data and the answers. The human touch is spent only on what genuinely needs us looking at real extracted output, not on re-asking what a form already captured.
