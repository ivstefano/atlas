# Schneider Electric deep dive, 2026-10-20 14:00-14:45 Sofia

Sources: Eric Slack recap (20 Oct), HubSpot deal 65887344024, calendar, Anita Slack (17 Oct). No transcript of the 12 Oct intro in Tactiq or Drive.

## Logistics (check first)
- TWO links. Kiran sent his own Teams invite (organiser = Kiran), same slot. Use Teams. Velislav's Meet link is likely dead.
- Kiran: "we will have to record this meeting as we have national holiday". Possible Kiran attends partly or watches later, others from his team may join. Recording = say nothing you don't want forwarded inside Schneider.
- Vankata (ivan_tsenov) has NOT accepted either invite. He's the tech answer for topic 1. Confirm he's on.
- Velislav (deal owner) is on the Meet invite but not on Kiran's Teams invite. Forward him the Teams link.

## Who / what
- Kiran Vyas, Head of BD, Process Automation India (Invensys side). Door-opener, not buyer. Judges fit, then hands us to the Schneider team that owns the problem + budget.
- Schneider builds its own AI, bought Cognite (USD 3.1bn, into AVEVA). They buy "already trained" capability to skip learning time.
- HubSpot: SQL stage, EUR 50k placeholder POC. Missing: owning team, use case, metric, budget, buyer, timeline.

## Goal of the call (one line)
Leave with: one use case Kiran likes + the name of the Schneider team that owns it + an intro to them.

## Layman decoder
1. "Govern AI across countries" = when the AI runs in India, Germany, US, where does the data sit, who can read it, which country's law applies. India has its own data law (DPDP Act 2023) and likes data kept in India.
   Our answer: it runs inside THEIR infra (their servers or their cloud region, e.g. AWS Mumbai). Data never comes to us. No Iris.ai off switch. Access by role, everything logged.
2. "Stop non-subscribers taking AI advice" = the AI's answers are valuable. How do you stop someone not paying (competitor, ex-customer, a user without a licence) from getting or copying them?
   Our answer: answers only exist inside their deployment, behind their login and roles. Who asked what is logged. Anything beyond that (watermarking, per-answer licensing): don't guess, Vankata or follow-up.
3. "Data poisoning" = someone feeds bad data so the AI learns wrong things or gives wrong advice. Schneider's trick since 2018: layers pass only short conclusions ("pump 3 running hot"), never raw data. Less to tamper with, cheaper.
   Our answer: our knowledge layer cites the source document for every answer and scores answers (built-in evaluation), so a bad answer is visible and traceable.
4. "Interoperable ecosystem" = partner AI must plug into Schneider's AI cleanly, not as a separate island.

## Topic 2: top 5 use cases (proof, no client names on a recorded call)
1. Steel plant machine knowledge: live work with a European steel plant builder, now in stage 2 implementation. Kiran named steel. Lead with this.
2. Telecom contact centre: telco ontology work + context layer for customer service agents. Kiran named it.
3. Engineering drawing extraction: weld data from weld drawings, scanned plates.
4. Commercial document extraction: automotive supplier contracts, 99.6% vs their expert's numbers.
5. Cross-department engineering data layer / production quality correlation (industrial manufacturer).

## Topic 3: India capability (the gap, say it straight)
- No India office. Don't promise 10-15 years of direct support.
- Frame: partner-led. We train Schneider's or an Indian partner's team, they run L1/L2, we stay L3 + product. Deployment in their AWS region.
- Line: "I'd rather be straight with you: we don't have a team in India today. Here's what we'd do: train your people in phase 1, and we stay behind them on the product."
- Long support asks = Jordan/Velislav commercial, park it.

## Pocket lines
- Don't-guess: "Good question. I don't want to guess, I'll get you the real answer by Thursday."
- Real vs roadmap: "Let me be precise about what's live versus what we'd build for you."
- Close: "Which Schneider team owns this problem, and could you introduce us? I want to build for the right person."
- Next step: "So next step: [use case] one-pager, by [date], and [team] decides. Did I get that right?"

## Parked / not today
- Joint paper for Indian govt on AI law: nice, not a deal. Acknowledge, don't own it.
- Cognite overlap: positioning has to be precise, don't trash them (Schneider owns them now). Anita has a warm line to Cognite's ex-CEO John Lervik if useful later.
- HubSpot ACE sync failing on India postal code for this deal (admin, not for the call).
