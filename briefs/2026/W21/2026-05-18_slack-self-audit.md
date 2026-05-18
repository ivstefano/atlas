# Slack self-audit, 2025-11-04 to 2026-05-18 (~6.5 months at IRIS)

Generated 2026-05-18. Smart-scoped pull: your sent messages across all conversations + targeted DMs/threads with senior peers (Jordan, Steven, Viktor, Vankata, Ivan T, Ross), engagement channels, and #commercial / #sales / #gtm-team / #neuralith. Skipped #random, #tech research-team channels, bot DMs.

Quotes are direct, with permalinks where useful. Where the original is Bulgarian I include a short translation.

---

## TL;DR

You produce, ship, and communicate a lot. The chaos you sense is real, but it's not coming from your output. It's coming from three structural patterns:

1. **You over-apologize for things that aren't your fault.** This makes you look junior and unloads accountability onto you from others.
2. **You communicate operationally (tactical, in-the-moment), not strategically (status, framing upward).** Steven and Viktor consistently have to ask "what's the state of X?" because you don't push that signal up. You wait to be pulled.
3. **You are the human glue between commercial (Jordan) and tech (Vankata/Viktor/Ivan T)**, but the role isn't named, the responsibilities aren't written down, and you absorb the friction silently in your Vankata DM at 16:00 BG instead of structuring it. Vankata on 2026-05-15: *"тези неща трябва ти да колаутваш, защото иначе ставам пъдар"* ("you need to escalate these things, otherwise I become the bad guy").

The good news: you're already aware of (3). Your atlas/engagements repo work, Asana migration, and HubSpot MCP push are the right structural fix. The rest of this report is about (1) and (2) plus the chaos-reduction question you asked at the end.

---

## Lens 1: How you write (style audit)

### What's working

- **Multi-channel summaries are good.** When you take time, your status updates are well-structured (numbered, with "Where we stand / Timeline I'm thinking / What I want to confirm"). The 2026-04-29 Heineken Justyna summary, 2026-04-29 Heineken weekly DM brief for Jordan, 2026-03-19 Aumovio evaluation-files summary are the model.
- **You handle escalation calmly under pressure.** Your 2026-04-28 Postbank "Going there right now, please stand by → we're here but it's a big building → got in contact" sequence is composed and useful while also losing a client in a building.
- **You give credit publicly.** Your 2026-04-20 "Great work and great demo on the file upload links. Kudos to @Yevhenii and @Vladimir" is the kind of thing that compounds — multiple peers are warmer to you because you do this consistently.
- **You document for re-use.** The 2025-12-12 #marketing demo summary (screenshots + narrative + Drive link) is exactly how a senior solutions architect ships internal artifacts.

### What's hurting you

#### Over-apologizing

You used the word "sorry" or "I'm sorry" or "sorry guys" **at least 50 times** in 6 months, almost always for things that are not your fault. A sample from the search:

- 2025-12-10 to Liana: *"Sorry working hard on 2-3 fronts."* — you're working hard, that's not a thing to apologize for.
- 2025-12-12 to Yevhenii: *"sorry for the late reply"* + *"too many conversations with clients"* — context is good; apology is unneeded.
- 2026-01-28 to Liana: *"I'm really sorry, I told Jordan and Vankata, but they're still talking, coming in 1-2 min"* — not your delay.
- 2026-02-12 to Steven: *"Sorry Steven it was 18:30 my time and I was not aware I had to join just now seeing the message"* — 18:30 is past your working hours, you owe no apology.
- 2026-04-23 to Yevhenii: *"sorry I'm not trying to be difficult"* — you were asking a reasonable design question; apologizing here trains the other side to push back harder.
- 2026-05-11 to Marti, Heineken: *"Hi Marti, first of all thank you for flagging this, it's really important and I have given you old information. Here's what actually matters..."* + *"I'm sorry for that once more :disappointed:"* — the first half is great (you correct yourself, thank them, give the right answer). The second message dilutes it.

Pattern: when something is genuinely your mistake, **a single, factual "I gave you old info, here's the right one"** lands as senior. The repeated apology lands as anxious. Senior peers absorb this signal without realizing it.

#### Hedging and softening

You routinely soften statements that would be stronger as assertions:

- *"I guess..."* (60+ uses)
- *"maybe..."*
- *"I'm not sure, but..."*
- *"sounds good"* / *"good stuff"* (filler agreements that don't add anything; OK once or twice per thread, not every reply)
- *"Just a quick question..."* before a substantive question

In Bulgarian DMs with Vankata + Ivan T you don't do this. You write directly. The hedging is mostly an English-with-senior-peers tic. Worth fixing because Steven, Viktor, and Jordan read English-you, not Bulgarian-you.

#### Reply-fragmentation

You frequently send 5-15 short messages in a row instead of one composed message. Example: 2025-12-12 with Yovcho (24 micro-messages in 30 minutes). Example: 2026-05-15 with Vankata about an Arcade-demo access problem (50+ messages, 90% one-liners).

Cost: in Slack history (and in someone else's notifications), this reads as "Ivo is panicking" or "Ivo can't think clearly". A composed 4-line message saying *"Trying to share the Arcade demo with you, getting 'view-only' from my side. What email did you use to register?"* would have closed the loop in 1 send.

This is the single biggest visible-style fix you can make. Aim for 1-3 messages per logical turn, not 10.

#### Late-night and weekend sends

Search returns dozens of sends from you at 23:00+ BG and Saturdays. e.g. 2026-05-14 22:19 to Aleks, 2026-05-15 16:40 to Vankata. Your working-hours memory says ~40hr/wk and you wanted "calm flow". The pattern in Slack does not match that aspiration yet. Two reads:

1. You're working late genuinely. The recovered-calm framing isn't real yet.
2. You're sending late so people see it next morning, which trains them that you're always-on, which trains them to ping you outside hours.

Either way: schedule-send for 09:30 BG next-day. Slack supports it natively. Or save drafts.

### Recommendation summary — Lens 1

| Stop | Start |
|---|---|
| Saying "sorry" reflexively when no actual error | Saying nothing or "Quick context: ..." |
| Hedging with "I guess / maybe" when you actually know | Direct statement; flag genuine uncertainty separately |
| 10-message bursts | 1-3 composed messages per turn |
| Late-night sends | Schedule-send for morning |
| "Sounds good" / "Great" filler-replies | An emoji reaction or nothing |

---

## Lens 2: What you own vs delegate vs miss (ownership patterns)

### What you own (consistently and well)

- **Engagement-level operational coordination.** Aumovio, Heineken, SMS Group, DB InfraGO, Postbank, TandF, Garrett: you are the connective tissue. Every meeting agenda, every Drive upload, every demo recording, every status update to Jordan/Steven runs through you.
- **Translating between tech and commercial.** Your 2026-01-28 Vankata DM ("Аз като човек между двете страни виждам, че Джордан гледа на нещата като ... докато инженерният екип го вижда като ...") is the clearest articulation of this role I see in 6 months. You see the gap. You named it to Vankata. But you didn't propose the fix.
- **Prep work and presentations.** You consistently are the one writing decks, walking through scoping presentations, and being on the screen during demos.
- **Tooling and infra for yourself.** atlas repo, engagements repo, /morning-brief, Asana commercial tracker, the HubSpot MCP push — you are quietly building IRIS's internal SA operating system. This is high-leverage work that nobody else is doing.
- **Drive hygiene.** You're the only person reorganizing the shared Drive into a coherent structure (Commercial/POC layout, drive_ids, $IRIS_EVERYONE convention). Nobody asked you to. It's saving the org dozens of hours/quarter.

### What you delegate (and how cleanly)

- **Frontend implementation.** You hand off cleanly to Yevhenii / Volodymyr / Romek / Vladimir with screenshots and reproduction steps. Your 2026-02-18 Asana bug ticket for Denis + Yovcho is exemplary: video, expected, current, ticket link.
- **Deck visual polish.** You correctly recognize Jordan is faster on this. You write content, hand over for polish.
- **Legal/NDA.** You started doing this yourself (2026-05-15 with Ivana: *"извинявам се не съм свикнал с процеса"*), realized mid-conversation it's Ivana's responsibility, and re-routed. Good adjustment.

### What slips through (the "miss" lens)

This is the highest-value section. Patterns where work falls between the cracks or stalls waiting on you:

#### 1. You don't push status upward unless asked

Steven 2026-04-07 #mpdm: *"Hi, Ivo, when you are free, I need an update on Aumovia in terms of PoC completion?"* — he had to ask. Steven 2026-04-27 DM: *"Ivo, is this still your tracker?"* — he didn't know if the tracker was current. Steven 2026-01-21 DM: *"Ivo, so which platform we can show now, is the above demo environment is still okay?"* — he didn't know what was live.

This is the same pattern three times across three months. Steven (CRO) doesn't know the state of your work because you don't put it in his face. Your morning-brief loop is the right answer (he gets the digest), but it's not yet running, and even when it does you need to push the digest to him, not wait for him to read atlas.

**Action**: until the morning-brief is automated to Slack-DM, send Steven a Monday 2-paragraph status by 09:00 BG every week. Even just copy-paste from the commercial-call brief.

#### 2. You absorb organizational dysfunction silently in DMs

Your 2026-01-28 Vankata DM about Jordan-vs-tech role friction. Your 2026-05-15 Vankata DM about the SMS deck Jordan led, where Jordan said "I haven't had visibility on progress for 2-3 weeks" in the group chat after you and Vankata flagged it privately for months. Your 2026-04-29 Vankata DM: *"Ами да като цяло малко се чувствам, че съм пуснат да се оправям"* ("I feel a bit like I've been thrown in to figure it out alone").

You correctly identify these tensions. You correctly tell Vankata. You don't escalate to Viktor or Steven, and you don't name them in writing in a place where they get fixed. Then they explode 6 weeks later in front of everyone in the SMS group DM.

**Action**: when you spot a structural problem, write a 1-page doc (you have the engagements repo, use it: `_live/ways_of_working_<topic>.md`). Send to Vankata first, then to Viktor or Steven. Do this within 48hrs of noticing, not 6 weeks.

#### 3. You wait for permission on things you should just do

- 2026-01-30 #mpdm: *"At this point Axion could ingest the investigation files... :smile:"* — you have an idea, you crack a joke, you don't propose it formally.
- 2026-04-29 Heineken neuralith-poc: *"I could use some guidance on this, both on whether the scope feels right..."* — you laid out a complete plan, then asked permission. Lucy and Justyna would have accepted what you proposed; Vankata would have approved.
- 2026-05-15 #tech: *"What are top 3 impactful things that need to be improved right now?"* in response to Ivan T asking for a list — you turned it back into a question instead of just suggesting 3.

Pattern: you have the judgment. You have the data. You ask for permission when you should be recommending.

**Action**: when you have a complete proposal, lead with "Recommendation: X. Reason: Y. Need: Z by [date]." Save "Open to feedback" for the genuinely uncertain parts.

#### 4. Drive/file org work is invisible because you don't publish it

The Drive reorg you did 2026-05-16 to 2026-05-17 (Aumovio move, SMS Group reorg, Heineken orphans upload, Scoping Exercises subfolders for 7 engagements) is 1-2 days of senior-SA work that nobody knows about. It's in `STATUS.md` files and `_aliases.yaml`, neither of which Steven reads.

**Action**: once a week, a 3-bullet "infra wins" post in #commercial or #gtm-team. Not selling yourself, surfacing the work so it counts.

---

## Lens 3: How others perceive your work (peer feedback)

### Positive

- **Steven 2026-02-10 #marketing**: *"Checkout the work that Ivo & Jordan pulled this together to show customer what we can do immediately, in which this is also turning into another PoC for us (Yes, another lighthouse customer)... Great work!"* — public commendation to Liana, refers to a PoC that materialized from your work.
- **Steven 2025-11-12 #mpdm**: *"I will start integrating your slides Ivo into one single partnership deck, in which many of these content (or subset of it) will go into the partnership website page."* — your content used by CRO for public-facing partnership deck. Strong signal early on.
- **Yevhenii 2026-03-03 DM**: *"Happy Birthday, Ivo! Wishing you good health, love and peace! Have a great day!"* — peer warmth. The whole #irisaibg / Vankata / Ivan T / Yevhenii / Vladimir cluster is consistently warm with you. You're well-liked by the people you actually work with.
- **Viktor 2026-04-08 #mpdm**: *"But I dont think I have much to add to what Ivo said"* — small but telling. Viktor is a strong opinion-haver. When he defers, it means you covered the ground.
- **2026-05-15 #commercial.** Liana 2026-05-13: *"@Ivo please join the podcast call ASAP"* — Liana pulls you in when she needs a competent face, not just because you're available.
- **Vankata 2026-05-14 DM**: *"много добре си го направил, ние бяхме искрено впечатлени"* ("you did this really well, we were genuinely impressed", on the DB demo).
- **Vankata 2026-05-15 DM** (re your atlas/engagements work): *"Ще е мнн яко"* + *"Страхотно, ако може това да се закача за хъбспот и асана"* ("It'll be really cool, awesome if you can hook this into HubSpot and Asana") — your CPO is endorsing your infra work.

### Critical (rare, direct, fair)

- **Steven 2025-12-07 DM**: *"Ivo, I included you in one of the meeting tomorrow, for a potential customers who is looking to build variety of agents to support their banking system."* — Steven invited you into a banking deal. (Postbank ultimately came from this kind of thread.) The pattern: Steven gives you scope. He expects you to ship without follow-up nagging.
- **Jordan 2026-02-02 #mpdm**: *"Vankata can you brief Ivo? I'm in meeting"* — Jordan delegates briefing you instead of doing it himself. Worth noting: when you're not at a meeting, you need to be the one asking for the briefing, not waiting for one to be offered.
- **Vankata 2026-05-15 DM (re your behaviour during SMS-deck issue with Jordan)**: *"тези неща трябва ти да колаутваш, защото иначе ставам пъдар"* ("you need to escalate these things, otherwise I become the bad guy") — direct feedback: when there's a problem with Jordan's work, Vankata wants you to surface it, not him.
- **Vankata 2026-05-15 DM (same conversation)**: *"просто трябва да е много конкретен аск, и много ясни цитати за behavior-а"* ("the ask has to be very specific, with very clear quotes of the behavior") — Vankata is telling you how to escalate effectively. He's giving you a playbook.
- **Ivan T 2026-03-31 #mpdm**: *"I hope Ivo can handle this, since I have a call with the EIC now"* — Ivan T trusts you to handle without him. That's a vote of confidence, but it's also a hand-off. The risk: if you don't ship, it lands on his record too.

### Read across the feedback

You are **trusted and well-liked**. Vankata, Steven, Viktor, the tech team all give you space and credit. The critical feedback is operational ("update me", "escalate this", "be specific in your ask"), not character or competence. That's the best critical feedback to get — it's all fixable.

The thing nobody has said out loud but is visible in the data: **they don't see you as someone who pushes upward yet.** You're seen as a reliable hands-on operator. Steven gives you tracker requests. Jordan gives you tasks. Vankata gives you protection. None of them is yet treating you as someone who decides the *shape* of work — they treat you as someone who executes it well. Your atlas/engagements work, the Asana migration push, the HubSpot work, the morning-brief loop, the channel reorganization proposal at today's commercial call — these are the leverage points to change that perception.

---

## Lens 4: Gaps — what's missing

### 1. No outward weekly status

You don't post a "here's what I did this week / here's what's next / here's where I'm blocked" anywhere. Steven asks twice for trackers, Jordan asks for briefs, you handle each individually. Recurring post = 10 minutes Friday afternoon = saves you 30+ min/week of these individual answers.

### 2. No proactive escalation to Viktor / Steven

In 6.5 months your DMs to Viktor are tactical (HubSpot permissions, Claude purchase approval, security questions). Zero "Viktor, I think we have a structural problem with X, here's what I'd do." Steven gets occasional 4-bullet updates but only when invited. Both of these people are explicitly there to unblock you. You're under-using them.

### 3. No public surfacing of your tooling work

atlas + engagements repos are the most original work being done at IRIS that isn't a client deliverable. Steven and Jordan don't know what's in them. Aleksandar (2026-05-14) is the first non-Vankata person you sent the engagements repo link to. Document it once in a #gtm-team or #commercial post: "Here's the atlas + engagements operating system, here's how to use it for your next engagement, here's the slash commands." One post.

### 4. No client-facing reference quotes / case studies pipeline

The Heineken Phase-2 brief includes Jordan's 2026-04-30 reference-quote ask from Lucy. You haven't owned that. Garrett showcase v3 + DB InfraGO 96.6% groundedness + Aumovio V5 + Heineken PoC wrap-up are all candidates for sanitized case-study content. You'd be the natural person to own the IRIS solutions-case-studies repo. Even if it doesn't exist yet, propose it.

### 5. No after-action / retro discipline

When a deal closes-lost (Agrolimen 2026-05-15) or a deal is in crisis (SMS deck 2026-05-15), there's no "what would we do differently" doc. Vankata and Steven both explicitly asked for one in the SMS thread. Even a 1-page retro per closed deal would compound into a playbook over 12-18 months.

### 6. No "I am off / OOO" comms discipline

Pattern: you're on vacation, someone DMs you, you reply *"Sorry man, I'm on vacation, Vankata is your guy"* (2025-12-19 to Jordan). The apology again, and reactive. Slack supports an OOO setting + a custom status. Use them. Vankata, Steven, and Jordan will respect them.

---

## Lens 5: Chaos reduction (your bonus question)

You asked "how can I improve others' work?" Here's where you have actual leverage:

### Things you can fix that compound across the team

#### A. Naming the SA role formally

You sit between commercial (Jordan), product (Vankata), eng (Petar, Martin, the Ukrainians), and revenue (Steven, Viktor). Nobody has written down what a Solutions Architect at IRIS does and doesn't own. Without that:
- Jordan thinks you do scoping calls + demo prep + commercial follow-up.
- Vankata thinks you do tech-commercial translation + scoping + delivery oversight.
- Steven thinks you do client tracking + deck content + tracker updates.
- You think you do all of the above plus the engagements/atlas infra.

Propose a 1-page "SA role at IRIS" doc to Vankata. He's CPO. He'll back it. This sets up the conversation about hiring a second SA (which is coming whether IRIS plans for it or not).

#### B. Engagement-channel policy

Half of IRIS's engagements live in group DMs (SMS, Garrett, DB, TandF, Postbank, Fresenius). Half live in channels (Aumovio, Heineken, Yettel). Asymmetric and indefensible. Propose at today's 12:30 commercial call: every active engagement = a `#<eng>-poc` channel by EOW. Owner: you. Deadline: Friday 22 May.

This is the single biggest "make everyone's work less chaotic" win. Steven and Viktor get search-able history. Tech team gets context. You stop being the historian.

#### C. Working hours and review-cycle discipline

The SMS-deck thread on 2026-05-15 is a case study in this failure. Steven said the right thing: *"I don't think we should have less than 1 full calendar week between final alignment meeting and deliverable due-date for major proposals, ideally 2 weeks."* Nobody owns enforcing this. Propose a deal-tier policy (Tier 1: 2-week review minimum; Tier 2: 1-week; Tier 3: 48hr) and bring it to Monday commercial calls. Vankata mentioned wanting this too.

#### D. Meeting-recording discipline

You repeatedly miss things because you weren't in a meeting and there's no record. 2026-01-29 *"Sorry guys, I didn't know we had it, already went out of the office"*. 2026-03-09 *"Може ли да те помоля ако правите среща с Торстен тази седмица да я запишете, защото съм off"*. 2026-04-29 *"Could you please send me a transcript of the Postbank call we had yesterday?"*.

Solution: every external client meeting gets Gemini Notes ON. Internal policy, not optional. The IRIS.ai HubSpot bot is supposed to do this; Ivan G. permission ask (today) is the blocker. Make this a policy item, not a one-off favor.

#### E. Asana hygiene

You bootstrapped the commercial tracker last weekend. Good. But it'll rot in 4 weeks if every engagement owner doesn't update their section weekly. Propose: every Monday by 11:00 BG, owner updates their Asana section. If not updated, the engagement isn't on the 12:30 call agenda. Hard rule. Vankata will back it.

---

## Top 5 actions for next 14 days

Ranked by leverage:

1. **Today, 12:30 commercial call**: propose engagement-channel migration policy. Owner: you. Deadline: Fri 22 May. (Lens 5B)
2. **This week**: write a 1-page "SA role at IRIS" doc. Send to Vankata first. (Lens 5A)
3. **Friday 22 May, 17:00**: first weekly Slack post in #gtm-team or #commercial — "What shipped this week, what's next, what's blocked." 8 lines max. Repeat every Friday. (Lens 4.1)
4. **This week**: stop apologizing reflexively. Pick 3 messages where you'd normally say "sorry" and don't. Notice what happens. (Lens 1)
5. **By 2026-05-25**: write a 1-page Agrolimen close-lost retro. Send to Vankata + Jordan + Steven. (Lens 4.5) Bonus: do same for any other closed-lost since you started.

---

## Things you should NOT change

- Your warmth with the tech team. Yevhenii, Vladimir, Vankata, Ivan T all genuinely like working with you. That's a moat.
- Your tooling instinct. atlas + engagements repo + Asana + HubSpot push + morning-brief. Keep building.
- Your bilingual register. Bulgarian with Vankata + Ivan T is correct and human. English with Steven + Jordan is correct and professional. The split is fine; the gap between them isn't (see Lens 1 hedging).
- Your willingness to take messy work nobody else wants (Drive reorg, NDA process cleanup, engagement-folder convention). This is real seniority showing.

---

## Open questions for you

- Want me to draft the SA-role doc as a starting point?
- Want me to draft the Friday-weekly Slack template?
- Want a `/slack-weekly` slash command that auto-pulls your week's activity into a draft?
- Should this report be memory-persisted (top 3-5 patterns saved as auto-memory) so future sessions catch when you slip back into these?

*Source corpus*: ~500 of your sent messages across 5 time-slices Nov 2025 → May 2026, plus targeted threads from senior peers + engagement channels. Direct quotes verified, permalinks available in source data if needed. Bulgarian translations preserve intent but not literal phrasing.
