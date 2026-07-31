# Pass 2 questions

For the Neuralith onboarding upload flow. Each question below has the reason we ask it, so the form can be built to fit the answer we're actually after.

Group A is quick and factual. Group B is the part that needs the uploaded files on screen next to it.

---

## Group A: Factual (things the files don't tell us)

**A1. What languages appear in these documents?**

The reason we ask is to know whether we should be doing translation to English or not. European languages are usually easier to handle, but it makes a real difference if there's Cyrillic, Arabic or something from the Asian group in there. Worth grouping by script rather than by country, so we get that answer directly instead of working it out ourselves from a list of countries.

**A2. Do your documents all follow the same layout and format?**

We ask this because we want to know if we're dealing with one template or with totally different file types and layouts. One standard form is a straightforward job. Every source looking different is a much bigger one, and we'd rather know that before we quote.

**A3. How many documents do you need to process beyond the uploaded ones?**

This tells us what the full implementation actually looks like. It could be a few hundred, a few thousand, or hundreds of thousands, and those are different projects. Also worth separating a fixed pile from documents that keep arriving: a backlog is a one-off run, a continuous flow is a recurring service.

**A4. Where do these documents live today?**

Determines whether the real implementation needs an integration or stays a manual upload. If everything sits in SAP or SharePoint, that's a connector and a different quote. Scanned paper tells us OCR is unavoidable.

**A5. Where should the project run?**

Some customers strictly require the project to run on their own system or on-premise, while others are fine if we run it on our AWS infrastructure and take advantage of the credits we have through our collaboration with Amazon. Big difference in both cost and setup time.

**A6. What needs clearing before the real data can move?**

In a lot of cases an NDA has to be signed or a security review has to pass before real data moves, and that's usually what sets the start date rather than anything technical. Vendor onboarding on its own can take a month.

**A7. Are the files you just uploaded the real thing, or samples?**

Often the person filling this in has uploaded examples just so we can show our capabilities, and a different employee has access to the real project data. We need to know that now, and get that person's name, because otherwise every file goes through a relay and we lose weeks.

**A8. Do you have a template or schema the output has to match?**

The documents tell us what goes in, never what should come out. If they already have a spreadsheet or a schema the result has to fit, that defines the whole job. If they don't, we propose one. We just need to know which of the two we're in.

---

## Group B: Detailed (about the real job, not the ideal one)

These sit next to the uploaded files on purpose.

**B1. The last time someone did this by hand, what happened? Which document, what did they type where, how long did it take?**

We want the job as it's actually done, not the ideal version. Asking about one real past instance gets a truthful answer; asking how the process works gets a description of how it's supposed to work. The time it takes is also our baseline for what we're saving them.

**B2. Pick one document you just uploaded. What's the right answer for it?**

This is the question the whole two-pass structure exists for. Naming their own file back to them makes it concrete, and one worked example tells us more about the target output than any amount of abstract description. The file list here should come from what they just uploaded.

**B3. To get that answer, did you need anything not printed on the page? A conversion, a rule you always apply, a judgment call?**

This is where the hidden business rules come out. There's almost always something the SME applies automatically and has never written down, and if we don't catch it here we find it later as an accuracy problem.

**B4. Do your documents ever contradict each other, and how do you resolve it?**

Documents disagreeing with each other is common and it forces a decision we can't make for them. When two parts of the same file say different things, we need to know whether to pick one or flag it and leave it blank. Getting that rule now stops us guessing wrong across thousands of documents.

**B5. Who checks this work today, and what counts as a mistake when they do?**

Not all errors are equal and only they can tell us which ones matter. A wrong number in a regulatory field can be a liability; different wording usually isn't. This is what we tune against, and it's also who we'll be judged by.

**B6. In the files you uploaded, is the correct answer already filled in anywhere?**

Without a correct answer to compare against we can't put a number on accuracy, we can only show output and ask whether it looks right. If they already have the answers we can measure properly from day one. If they don't, someone on their side has to produce them, and that's work to plan for rather than discover halfway through.

**B7. If the pilot works, who owns the budget: the same person filling this in, or someone else?**

The person who fills this in usually isn't the one who can approve spend. Knowing early who does, and whether it's one person or a committee, tells us who needs to see results and how long the decision will take.

---

These are the questions that stall scoping when asked out of the blue. Combining them with the uploaded files is what makes them answerable: the client discovers their own gaps while filling this in, instead of us discovering them three calls later.
