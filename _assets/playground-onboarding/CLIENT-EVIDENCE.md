# What clients actually ask for when they look at extracted data

Ranked by how many distinct client accounts raised each theme unprompted.

Read from every client transcript on file: **26 accounts, 41 meeting sets, about 1.15 million
words**. Counts are **distinct client accounts** whose own people raised the theme, never the
number of times it was said. Vendor-side speech was excluded.

**How to read each entry.** The finding comes first: what clients want and what it means for the
design. The quotes that support it sit underneath, so you can check the claim against what was
actually said. Quotes are tidied into readable English from auto-transcription; the sense is
faithful but the raw lines are rougher (see [Quote fidelity](#quote-fidelity)).

---

## Worked example: how this reads in practice

This is the pattern used for all twelve entries below. Same one from the call.

### The finding

Clients do not trust a value they cannot trace. Not because they doubt the technology, but because
they have to defend the number to somebody else. Traceability is what turns extracted data into
something a person will put their name against.

### What it changes in the UI

Every row opens the filing it came from. Every value shows the verbatim source text it was read
from, and says whether it was stated in the document or calculated from it. A cell with no source
is a cell nobody will sign off.

### What clients said

> "We can build that trust only if an end user can easily trace back the result, or see the
> source."
> — **Heineken**, Manager, Augmented Analytics & Insights

> "Is this extracted from the text, or is it actually a calculation?"
> — **Heyne Tillett Steel**, CTO, pointing at a single number on screen

> "The expert needs to be confident, and to have his assistant dig into the data source."
> — **SPIE**, GSE lead

The SPIE story is the one worth telling out loud: their own domain expert was shown a correct
answer, said it was impossible, and only accepted it after they opened the source documents
together. The answer was right the whole time. What was missing was the means to check it.

---

## The ranking

| #  | Theme                                                           | Accounts |
|----|-----------------------------------------------------------------|----------|
| 01 | Replacing people reading documents and typing data into a table | 21       |
| 02 | Being able to check the result against the document             | 19       |
| 03 | Output another system can actually use                          | 15       |
| 04 | Accuracy, and how it was measured                               | 14       |
| 05 | **Seeing where each value came from** (first by function)       | 11       |
| 06 | Making different documents comparable                           | 12       |
| 07 | Flagging what is missing instead of guessing it                 | 12       |
| 08 | Understanding the client's own terminology                      | 11       |
| 09 | Reading what is not text: tables, charts, drawings, scans       | 10       |
| 10 | Getting the data out into Excel or SAP                          | 8        |
| 11 | Documents in languages the reader cannot read                   | 6        |
| 12 | Speed and volume                                                | 10       |

---

## 01 · Replacing people reading documents and typing data into a table — 21 of 26 accounts

**The finding.** The most universal thing clients say, and they lead with it unprompted, before
anyone asks about features. What they are buying is the removal of a job somebody is doing by hand
right now.

**What it changes.** The headline should name the work the table removes, not the volume it
processed. A count of artifacts describes the machine. Hours not spent reading describes the buyer.

> "We would need to talk with 112 salespeople all over the world, and have somebody — me — sitting
> there typing it all into an Excel file like an idiot, trying to bring it together in one sheet.
> That is impossible."
> — **Aumovio**, sales/strategy

> "They gave sales the task of putting all the information manually into a database. They have been
> at it for four months and they are still not finished."
> — **Aumovio**, sales/strategy

> "We are now the mother of Excels."
> — **Heineken**, Head of Cost & Value

> "A lot of effort goes into checking, validating and explaining numbers, rather than generating
> them."
> — **Heineken**, Cost & Value specialist

Also said by: SMS Group · Fresenius ×3 · Agrolimen · Deutsche Bahn · Nielsen · Garrett · SPIE ·
Welocalize · NHS · Postbank · HTS · Orascom · Barentz · Stepan · AlexFert · SimLab · Aramco ·
Orion Telekom

## 02 · Being able to check the result against the document — 19 of 26 accounts

**The finding.** Clients do not want to be told the extraction is good. They want to perform the
check themselves, in front of a sceptic. This is a sales requirement as much as a product one:
several clients said outright that the table is what they will use to convince their own colleagues.

**What it changes.** The table has to be built to be audited, not admired. This is the core
argument for showing real output instead of a tally of counts.

> "Just telling is one thing. Showing is much more convincing."
> — **SMS Group**, senior executive and budget holder

> "A table like this is excellent material to convince people. They can take a look and say: yes,
> that is the information we are looking for, that is what is written inside, that is what was
> extracted. It fits. Let's go."
> — **Deutsche Bahn**, Head of Algorithms

> "The only thing that would really stop this project is if our engineers say, well, that's really
> interesting, but it's all wrong."
> — **Deutsche Bahn**, Head of Algorithms

> "Before we blindly rely on whatever comes out, we should have somebody look at it, to be safe."
> — **Aumovio**, sales/strategy

Also said by: Heineken · Fresenius ×3 · Agrolimen · Nielsen · Taylor & Francis · SPIE ·
Welocalize · NHS · Postbank · Barentz · Stepan · AlexFert · Aramco · Orion Telekom

## 03 · Output another system can actually use — 15 of 26 accounts

**The finding.** The output is a starting point for something else, never a destination. Clients
have a BI stack, a database, an SAP instance. Beauty is explicitly not the ask.

**What it changes.** The value claim is that the data is now usable elsewhere, not that it looks
good here.

> "Does it have to be super pretty? The data is spat out and we can manipulate it behind the
> scenes. We have our BI, you have different tools. Getting at the data — that is what's
> important."
> — **Nielsen**, senior data leader

> "There is usually no inherent value in extracting data. The value comes from the applications we
> can build on top of it."
> — **Deutsche Bahn**, Head of Algorithms

> "The business problem is that the data is unstructured and someone really has to put it into a
> structured form."
> — **Fresenius**, Regulatory Information Management

Also said by: SMS Group · Heineken · Aumovio · Agrolimen · Garrett · Taylor & Francis · SPIE ·
GrantSpider · Shanghai Synocodes · HTS · Postbank

## 04 · Accuracy, and how it was measured — 14 of 26 accounts

**The finding.** Clients ask *how it was measured*, not for a number on a page. The follow-up
question is always about method, and an unbacked percentage invites exactly the question that
breaks the demo.

**What it changes.** No accuracy figure is cleared for this corpus. Do not put one on the page.
What can be said honestly is a property of the corpus itself: 376 pages, six languages, 42% scanned
with no text layer, structured without per-document tuning.

> "Accuracy around 70%? Then of course it is not up to the expectations of our engineering team,
> because as you can imagine, for engineers, if it is not 100% it is not correct."
> — **Garrett**, Head of AI and Data

> "You mentioned that with the AI model you reach a level of trust. How do you check that you have
> reached this level? What is your procedure?"
> — **SMS Group**, senior executive

> "Accuracy is definitely one of the main requirements, if not the top one. The robustness we
> expect is in the extraction model, rather than in having a very polished website."
> — **Agrolimen**, Digital Transformation

Also said by: SMS Group · Aumovio · Fresenius ×2 · Nielsen · Taylor & Francis · Welocalize ·
FedEx · GrantSpider · Shanghai Synocodes · HTS · Postbank

## 05 · Seeing where each value came from — 11 of 26 accounts, **first by function**

**The finding.** Fifth by count, but the only theme clients name as the *precondition* for the
others. Trust, checking and accuracy all resolve to it. At Fresenius it is not even a preference:
FDA submissions require hyperlinks from a claim to the batch data behind it.

**What it changes.** Per-value provenance, not per-document. It is not enough to say which file a
row came from; clients ask whether an individual number was stated in the text or derived from it.

> "We can build that trust only if an end user can easily trace back the result, or see the source."
> — **Heineken**, Manager, Augmented Analytics & Insights

> "Is this extracted from the text, or is it actually a calculation?"
> — **Heyne Tillett Steel**, CTO

> "What I am missing is searching for an item and showing where that item appears in the documents.
> That is really helpful for the end user."
> — **SMS Group**, engineering lead

> "We expect not only to get the information back, but also to refer back to the original images,
> so that the engineer is able to trust it."
> — **Garrett**, Head of AI and Data

> "Hyperlinking is one of the important criteria when we provide the dossier to the health
> authorities, especially the FDA. We highlight the batch number in blue, and when they click it
> they can go and see the batch analysis."
> — **Fresenius**, CMC regulatory writer

Also said by: Aumovio · Nielsen · Taylor & Francis · SPIE · SimLab / Valencia

## 06 · Making different documents comparable — 12 of 26 accounts

**The finding.** Value appears at the moment documents stop being separate. Until then a client has
a pile of files; afterwards they have a dataset.

**What it changes.** Same columns for every document, differences readable down each one. Units
harmonised before display, because weekly, quarterly and lifetime figures are not comparable as
written.

> "We want something harmonised, where we have a yearly volume for all the products. It should be a
> yearly volume so we can compare it."
> — **Aumovio**, sales/strategy

> "I can see it goes a lot deeper into actually comparing. That's great."
> — **Agrolimen**, Digital Transformation — their only unprompted "that's great" of the call

> "One operating company has local systems and a specific data structure, the second has it
> differently. At global level I want to look at a unified KPI."
> — **Heineken**, Manager, Augmented Analytics & Insights

Also said by: SMS Group · Fresenius ×2 · Garrett · Taylor & Francis · GrantSpider ·
Shanghai Synocodes · HTS · Postbank

## 07 · Flagging what is missing instead of guessing it — 12 of 26 accounts

**The finding.** The most vehement theme in the corpus, and the one clients volunteer as praise
when they see it working. Coverage is negotiable. Invention is not.

**What it changes.** An empty cell reading "not stated" is a feature to show, not an absence to
hide. This is worth putting in front of the user rather than hiding behind a hover.

> "I like the 80% solution, because I would be fine with the 80% solution — at least if you don't
> have hallucinations for the other 20%."
> — **Deutsche Bahn**, Head of Algorithms

> "But this is just you guessing."
> — **Aumovio**, sales/strategy

> "If it is not there, we don't have it. Then it should be empty."
> — **Aumovio**, sales/strategy

> "A good point is that the AI is not trying to hallucinate something. It was saying: okay, this is
> not provided, there is a gap here. That is a positive."
> — **Fresenius**, Regulatory Information Management

> "If they don't explicitly say it is that subcomponent, then we can't assume it is. We only have
> the data in front of us."
> — **Fresenius**, post-market surveillance

Deutsche Bahn's operating rule explains why: no data means no rerouting recommendation. A fabricated
value is worse than a blank one, because it produces a decision. Taylor & Francis inverts the metric
for the same reason — recall must be 100%, precision may be lower.

Also said by: SMS Group · Heineken · Agrolimen · Nielsen · Welocalize · Shanghai Synocodes ·
Barentz

## 08 · Understanding the client's own terminology — 11 of 26 accounts

**The finding.** Not translation. Knowing that this field means the contracted volume and that one
means tooling, and that the same concept has a different name at every customer.

**What it changes.** The column header is the claim. Getting the label right is doing the work, not
describing it.

> "Whatever claim you extract from the paper without context is meaningless. You cannot say this
> drug is good for this disease. You need to say this drug is good for this disease, in this
> population."
> — **Taylor & Francis**, senior engineer

> "Maybe at other customers it is not called commodity name. Maybe they call it product, or article,
> or part. It could be many namings."
> — **Aumovio**, sales/strategy

> "I cannot even tell you what abbreviations all the OEMs use. Some of them just use an F and the
> other an R to distinguish. I really don't know how creative they are."
> — **Aumovio**, sales/strategy

> "You need to use the exact word. 'Exceeds', in this case, or 'remains available after'. From your
> answer I wasn't sure whether I have the budget or I'm missing it."
> — **Heineken**, Cost & Value specialist

Also said by: SMS Group · Deutsche Bahn · Fresenius ×3 · Agrolimen · Garrett · Welocalize ·
Shanghai Synocodes

## 09 · Reading what is not text: tables, charts, drawings, scans — 10 of 26 accounts

**The finding.** Tables, charts, schematics, drawings, handwriting. For several clients the
information they need is not in the prose at all, and often is not written anywhere.

**What it changes.** This corpus answers the question directly: 42% of pages are scanned images
with no text layer. That is the strongest single fact in the dataset and it is worth stating plainly.

> "If you only extract textual and table information, it's not enough, because the majority of the
> information is in the graphics. And the text is actually linked to the graphic close to it."
> — **Garrett**, Head of AI and Data

> "Drawings will not specify explicitly that this is the turbine, this is the hole, these are the
> dimensions. So how do we translate that into text? That is the biggest challenge we have."
> — **Garrett**, AI/IT project lead

> "When it is not human readable, I would say it is not machine readable anyway."
> — **SPIE**, GSE lead

> "Some are handwritten as well in the batch record, so you will see the handwritten ones."
> — **Fresenius**, CMC regulatory writer

Also said by: SMS Group · Deutsche Bahn · Agrolimen · Welocalize · Ahli Bank · FedEx · HTS ·
Postbank

## 10 · Getting the data out into Excel or SAP — 8 of 26 accounts, **a hard gate**

**The finding.** Lower count, but the only theme stated as a pass/fail condition on the whole
platform. This is the gap Michael identified on the call: the table does not show how it can be
used. The client evidence backs him.

**What it changes.** Show the exit. Export, or the handoff into the system the client already runs.

> "The main topic is this: if the platform can't export information via Excel, then it is not
> usable for SMS."
> — **SMS Group**, engineering lead

> "Can we have the output in a form that imports into SAP? That would be the final target for us,
> because we store the connected data in SAP."
> — **Aumovio**, project manager

> "Would there be an option to connect this with our CAT tool, so the extract can be added
> automatically?"
> — **Welocalize**, squad operations lead

Also said by: Deutsche Bahn · Heineken · Agrolimen · GrantSpider · HTS

## 11 · Documents in languages the reader cannot read — 6 of 26 accounts

**The finding.** Ranks low as a stated *requirement*, but it is what makes checking possible at
all. In the strongest instance the client could not verify his own contract because he could not
read it.

**What it changes.** Support the claim with a translated row beside its original, rather than a
language count in the headline. The count is a boast; the pair is proof.

> "At least I couldn't find it. Maybe it is hidden in the Chinese and I couldn't see it."
> — **Aumovio**, sales/strategy

> "Arabic is very dense, a very complex language. It works, but it is not as accurate as English.
> That is a challenge we already have."
> — **Ahli Bank**, Head of AI

> "I don't know so many different languages and formats."
> — **Agrolimen**, Digital Transformation

Also said by: Deutsche Bahn (German) · Heineken · Welocalize

## 12 · Speed and volume — 10 of 26 accounts, **deliberately last**

**The finding.** Clients raise scale constantly, but as the *problem statement*, not the buying
criterion. Two accounts argue against speed unprompted. This is consistent with the internal
position: we are not selling speed, we are selling accuracy.

**What it changes.** Scale belongs in the description of the problem, not in the promise. FedEx is
the single account that inverts this and wants real-time over accuracy.

> "It depends — we value quality more than speed."
> — **Shanghai Synocodes**

> "I did it on my own with limited means. That's fine, it's fun. But when you have two or three
> terabytes of data to process, the fun is lost. You can count it in days of processing."
> — **SPIE**, GSE lead

> "If you go to PubMed and search, you get 100,000 papers. No human is going to be able to get
> through those."
> — **NHS**, oncologist

Also said by: SMS Group · Deutsche Bahn · Heineken · Aumovio · Fresenius ×2 · Garrett · FedEx

---

## What the ranking means for the panel

The top four are all served by one decision: **show the finished table, not a count of what came
out of the machine.** Seeing where each value came from (row 05) ranks fifth on frequency but
first on function, because checking, trust and accuracy all depend on it — so per-cell provenance
and source text are load-bearing, not decoration. Empty cells stay empty and say so.

## What the corpus does not support

Three things worth knowing before they go on a page.

- **No client anywhere asked for a numeric confidence score.** They ask for flags, justifications
  and a source to open. Only one account ever named a percentage threshold.
- **Unit normalisation was never requested as a feature**, though Aumovio needs it done.
- **Multilingual quality is rarely a stated requirement.** Six accounts touch it, but most clients
  either work in one language or translate it themselves. It earns its place as the thing that
  makes checking possible, not as a headline claim.

## Read the counts honestly

They measure how many client accounts raised a theme, not how much it matters, and the corpus is
uneven: some accounts had a single intro call, others a year of delivery.

- Two contributed nothing usable: Yettel's transcripts are about a customer-service chatbot;
  Naturgy's folder is empty.
- Nielsen, Postbank and FedEx work mostly on structured data rather than documents, so their
  evidence transfers only in part.
- Deutsche Bahn and Agrolimen raised no OCR or scanned-document need at all, so row 09 rests on
  the other accounts.
- Where a theme is carried by one vivid account it is called out rather than ranked up.

## Quote fidelity

These are auto-transcribed calls, and the raw lines are rough: mangled words, dropped grammar,
names mis-heard. The quotes above are tidied into readable English. Meaning is preserved and
nothing was invented, but they are not literal transcript strings.

Two in particular read much more smoothly here than in the source: the Deutsche Bahn "excellent
material" line and the Agrolimen "goes a lot deeper" line. **Check the transcript before quoting
any of these back to a client or putting them in a deck.**
