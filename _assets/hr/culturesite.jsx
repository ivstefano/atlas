import React, { useState, useMemo } from 'react';
import {
  Users,
  ExternalLink,
  Compass,
  Search,
  Sparkles,
  BookOpen,
  CheckCircle,
  HelpCircle,
  Printer,
  Info,
  ChevronRight,
  ArrowRight,
  ShieldCheck,
  Zap,
  BookMarked,
  MessageSquare,
  Copy,
  Heart,
  Loader2,
  AlertCircle,
  RotateCcw,
  Send,
  Award,
  Activity
} from 'lucide-react';

// System prompt that feeds the entire PDF content into the Gemini LLM Context
const PLAYBOOK_CONTEXT_PROMPT = `
You are the Iris.ai Culture Companion, an expert organizational coach trained on the official Iris.ai Culture Playbook.
Your goal is to help team members act in alignment with Iris.ai values. Keep your tone supportive, highly professional, direct, and actionable.

Here is your reference documentation for Iris.ai principles:

1. HOW WE COLLABORATE INTERNALLY
- We communicate with clarity and intent: Speak directly, share context, make thinking visible. Share constraints early (time, data, trade-offs), explain "why" you propose something, and involve people early.
- We challenge ideas to improve outcomes: Welcome productive disagreement. Use evidence, data, or reasoning. Ask questions before rejecting, and separate ideas from the person presenting them.
- We create space for every voice: Actively include different perspectives. Invite input from quiet voices, avoid dominating discussions, and be mindful of different communication styles.
- We learn openly: Treat failures and outcomes as learning opportunities. Share what didn't work and why, run blameless retrospectives, highlight learnings over pure results.
- We build on each other's work: Document and share knowledge. Capture decisions, assumptions, and results. Write clear documentation for future scaling, share proactively.

2. HOW WE PARTNER EXTERNALLY
- We communicate proactively and transparently: Inform stakeholders early, especially when things change (risks, delays, slow progress). Don't wait until things escalate.
- We take ownership: Stand behind our work and delivery. Take responsibility for issues, focus on solutions over blame, and follow through.
- We act with professionalism and deliver commitments: Align on expectations early (kickoff/scoping), deliver work to agreed standards, communicate early if expectations must shift.
- We simplify complexity: Translate technical depth into clear, actionable insights. Focus on what it means, not just how it works. Adapt explanations to the audience. Replace jargon, use visual comparisons/examples, and summarize with: "What you need to know / What this means for you".
- We engage with professionalism and respect: Handle difficult discussions calmly, acknowledge alternative perspectives, and avoid defensiveness.
- We prioritize long-term trust over short-term gains: Don't compromise quality or safety to move faster under pressure. Be honest about feasibility, flag risks, recommend better alternatives.

3. HOW WE LEAD AND ENABLE OTHERS
- We create psychological safety: Ensure people feel safe to question/challenge. Respond positively when people speak up, normalize uncertainty/learning, and address dismissive behavior early.
- We lead by example: Demonstrate the behaviors we expect. Be transparent about your own decisions, admit when you don't know, and show absolute accountability.
- We enable growth and curiosity: Encourage trying new approaches, support learning beyond immediate tasks, and give space for exploration/reflection.
- We provide clarity and direction: Explain why decisions are made, communicate priorities/trade-offs clearly, and reduce ambiguity when teams feel blocked.
- We protect sustainable performance: Guard against burnout, challenge unrealistic timelines, encourage sustainable pacing, monitor team wellbeing.
- We develop people intentionally: Give constructive, actionable feedback, recognize contributions, adapt support in 1:1s, and mentor thoughtfully.
`;

// Playbook Static Dataset declared globally to prevent uninitialized reference errors
const PLAYBOOK_DATA = {
  internal: {
    title: "1. How We Collaborate Internally",
    subtitle: "We build trust through openness, respect, and shared ownership",
    color: "from-blue-600 to-indigo-700",
    accent: "#3C49CC",
    lightAccent: "#E2E1F3",
    principles: [
      {
        id: "i1",
        title: "We communicate with clarity and intent",
        desc: "We speak directly, share context, and make our thinking visible.",
        practices: [
          "Explain why you're proposing something, not just the outcome",
          "Share constraints early (time, data, trade-offs)",
          "Involve relevant people instead of working in isolation"
        ],
        triggers: [
          "During decision-making",
          "When priorities are unclear",
          "When something might impact others"
        ]
      },
      {
        id: "i2",
        title: "We challenge ideas to improve outcomes",
        desc: "We create an environment where disagreement is welcomed and productive.",
        practices: [
          "Use evidence, data, or reasoning to support your view",
          "Ask questions before rejecting ideas",
          "Separate the idea from the person presenting it"
        ],
        triggers: [
          "In design discussions",
          "When working across seniority levels",
          "When decisions have long-term impact"
        ]
      },
      {
        id: "i3",
        title: "We create space for every voice",
        desc: "We actively include different perspectives.",
        practices: [
          "Invite input from those who haven't spoken",
          "Avoid dominating discussions",
          "Be mindful of different communication styles"
        ],
        triggers: [
          "In group meetings",
          "In cross-functional collaboration",
          "When working with newer team members"
        ]
      },
      {
        id: "i4",
        title: "We learn openly",
        desc: "We treat outcomes—especially failures—as learning opportunities.",
        practices: [
          "Share what didn't work and why",
          "Run retrospectives focused on improvement, not blame",
          "Highlight learnings, not just results"
        ],
        triggers: [
          "After experiments or releases",
          "When something goes wrong",
          "When repeating similar work"
        ]
      },
      {
        id: "i5",
        title: "We build on each other's work",
        desc: "We document and share knowledge so it scales beyond individuals.",
        practices: [
          "Capture decisions, assumptions, and results",
          "Write documentation that others can understand later",
          "Share insights proactively, not only when asked"
        ],
        triggers: [
          "After completing work or experiments",
          "Before handing over work",
          "When working across teams"
        ]
      }
    ]
  },
  external: {
    title: "2. How We Partner Externally",
    subtitle: "We build trust through clarity, accountability, integrity and professionalism",
    color: "from-purple-600 to-indigo-800",
    accent: "#7F4F9F",
    lightAccent: "#E2E1F3",
    principles: [
      {
        id: "e1",
        title: "We communicate proactively and transparently",
        desc: "We ensure stakeholders are informed—especially when things change.",
        practices: [
          "Share risks, delays, or uncertainties early",
          "Don't wait until a problem escalates",
          "Provide updates even when progress is slow"
        ],
        triggers: [
          "Before deadlines",
          "When risks appear",
          "During long-running projects"
        ]
      },
      {
        id: "e2",
        title: "We take ownership",
        desc: "We stand behind our work and how it is delivered.",
        practices: [
          "Take responsibility for both successes and issues",
          "Focus on solutions, not blame",
          "Follow through on commitments"
        ],
        triggers: [
          "When something goes wrong",
          "When representing the team externally",
          "When decisions impact clients"
        ]
      },
      {
        id: "e3",
        title: "We act with professionalism and deliver on our commitments",
        desc: "We consistently strive to meet expectations and deliver the value we promise.",
        practices: [
          "Align clearly on expectations from the start",
          "Deliver work that meets agreed standards and objectives",
          "Follow through on commitments and timelines",
          "Communicate early if expectations need to shift",
          "Maintain a high standard of quality in all interactions"
        ],
        triggers: [
          "At project kickoff and scoping",
          "When delivering milestones",
          "When managing expectations under changing conditions"
        ],
        example: {
          label: "Communication Blueprint",
          text: "We're committed to delivering X by Y. Here's where we are, and here's how we ensure it meets expectations."
        }
      },
      {
        id: "e4",
        title: "We simplify complexity",
        desc: "We translate technical depth into clear, actionable insights that create value.",
        practices: [
          "Focus on what it means, not just how it works",
          "Adapt explanations to the audience (technical vs non-technical)",
          "Highlight implications, risks, and recommended actions",
          "Replace jargon with clear language and use comparisons"
        ],
        triggers: [
          "In client presentations",
          "In written reports or updates",
          "When explaining model outputs or limitations"
        ],
        example: {
          bad: "The model shows variance across subgroups due to distributional differences",
          good: "The model performs differently across user groups, which may lead to biased results in these scenarios."
        }
      },
      {
        id: "e5",
        title: "We engage with professionalism and respect",
        desc: "We handle discussions constructively, even when there is disagreement.",
        practices: [
          "Stay calm and solution-oriented",
          "Acknowledge different perspectives",
          "Avoid defensiveness"
        ],
        triggers: [
          "In challenging conversations",
          "When receiving criticism",
          "When aligning expectations"
        ]
      },
      {
        id: "e6",
        title: "We prioritize long-term trust over short-term gains",
        desc: "We don't compromise quality or responsibility to move faster.",
        practices: [
          "Be honest about what is feasible",
          "Flag risks instead of hiding them",
          "Recommend better alternatives when needed"
        ],
        triggers: [
          "Under deadline pressure",
          "When facing trade-offs",
          "When quality is at risk"
        ]
      }
    ]
  },
  leadership: {
    title: "3. How We Lead and Enable Others",
    subtitle: "We create the conditions for people and teams to thrive",
    color: "from-indigo-700 to-purple-800",
    accent: "#3C49CC",
    lightAccent: "#E2E1F3",
    principles: [
      {
        id: "l1",
        title: "We create psychological safety",
        desc: "We ensure people feel safe to contribute, question, and challenge.",
        practices: [
          "Respond positively when people speak up",
          "Normalize uncertainty and learning",
          "Address dismissive or harmful behavior early"
        ],
        triggers: [
          "In team discussions",
          "When someone raises concerns",
          "When mistakes happen"
        ]
      },
      {
        id: "l2",
        title: "We lead by example",
        desc: "We demonstrate the behaviors we expect from others.",
        practices: [
          "Be transparent about your own decisions",
          "Admit when you don't know something",
          "Show accountability in your actions"
        ],
        triggers: [
          "During uncertainty",
          "In high-pressure situations",
          "When setting team norms"
        ]
      },
      {
        id: "l3",
        title: "We enable growth and curiosity",
        desc: "We create space for learning and experimentation.",
        practices: [
          "Encourage trying new approaches",
          "Support learning beyond immediate tasks",
          "Give time for exploration and reflection"
        ],
        triggers: [
          "During planning cycles",
          "After project completion",
          "When people show initiative"
        ]
      },
      {
        id: "l4",
        title: "We provide clarity and direction",
        desc: "We align teams through context and priorities.",
        practices: [
          "Explain why decisions are made",
          "Clearly communicate priorities and trade-offs",
          "Reduce ambiguity where possible"
        ],
        triggers: [
          "When priorities shift",
          "During planning",
          "When teams feel blocked or unclear"
        ]
      },
      {
        id: "l5",
        title: "We protect sustainable performance",
        desc: "We actively guard against burnout.",
        practices: [
          "Challenge unrealistic timelines",
          "Encourage sustainable pacing",
          "Monitor workload and team wellbeing"
        ],
        triggers: [
          "During high-pressure periods",
          "When deadlines are at risk",
          "When workload increases"
        ]
      },
      {
        id: "l6",
        title: "We develop people intentionally",
        desc: "We support individual growth and strengths.",
        practices: [
          "Give constructive, actionable feedback",
          "Recognize contributions",
          "Adapt support in 1:1s",
          "Onboard and mentor thoughtfully"
        ],
        triggers: [
          "In 1:1s",
          "During performance discussions",
          "When onboarding or mentoring"
        ]
      }
    ]
  }
};

// Curated dilemmas used inside the upgraded AI Assessment tool
const ASSESSMENT_CHALLENGES = [
  {
    title: "Disagreement on ML Thresholds",
    pillar: "internal",
    context: "A senior researcher asserts that the classification threshold should remain at 0.85 to minimize false positives, but your benchmarks show 0.75 performs better on edge-case demographics."
  },
  {
    title: "Client Pressure on Early Launch",
    pillar: "external",
    context: "Our key enterprise client is demanding a production release by Friday afternoon, but you found minor bias drifts in subgroup tests that require 2 more days of validation."
  },
  {
    title: "Signs of Team Burnout",
    pillar: "leadership",
    context: "You notice our high-performing backend developer is pushing major pipeline refactoring commits at 3:30 AM over the past 3 consecutive nights."
  },
  {
    title: "ML Jargon in Stakeholder Review",
    pillar: "external",
    context: "Explain a 15% latency drop during high concurrency caused by 'anisotropic database embedding query decay' to the client's non-technical business executive."
  },
  {
    title: "Staging Pipeline Downtime Error",
    pillar: "internal",
    context: "A utility script you deployed to simplify dataset validation accidentally triggered a cascade failure, taking down the team's shared staging server for 4 hours."
  }
];

// THE 50 STATIC SCENARIOS DATASET declared globally to guarantee instant compile scope
const SCENARIO_GYM_LIST = [
  // INTERNAL COLLABORATION (1-17)
  {
    id: 1,
    pillar: 'internal',
    title: "Proposing a Transformer Architecture Switch",
    context: "You believe switching to a newly released Transformer layout will boost accuracy by 4%, but rewrite parts of our training pipeline. The squad is skeptical.",
    choices: [
      { id: 'A', text: "Write an RFC explaining 'why' you are proposing the switch, outlining benchmarks, computational overheads, and trade-offs.", correct: true, feedback: "Excellent! Sharing context, metrics, and constraints proactively embodies 'communicating with clarity and intent.'" },
      { id: 'B', text: "Quietly implement it on your local branch and present it as a finished accomplishment at the next general stand-up.", correct: false, feedback: "Working in isolation can lead to system conflict and limits shared squad ownership." },
      { id: 'C', text: "File an urgent Jira request stating that the old pipeline is suboptimal and must be modified immediately.", correct: false, feedback: "Directives without context or clear explanation ignore the requirement to build consensus through clarity." }
    ]
  },
  {
    id: 2,
    pillar: 'internal',
    title: "Unexpected Dataset Preprocessing Bottleneck",
    context: "During sprint planning, you realize compiling the CJK multi-modal testing vectors will take 2 weeks instead of 2 days, potentially delaying other tasks.",
    choices: [
      { id: 'A', text: "Wait until next week's stand-up to see if you can find ways to optimize the pipeline yourself first.", correct: false, feedback: "Delaying warnings leads to systemic bottleneck surprises. Proactive sharing is vital." },
      { id: 'B', text: "Flag the time constraint immediately, detailing the trade-offs between dataset coverage and milestone delivery.", correct: true, feedback: "Perfect. Sharing constraints early (time, data, trade-offs) allows the team to pivot safely together." },
      { id: 'C', text: "Work late nights in isolation to catch up, hoping to resolve the bottleneck without bothering the team.", correct: false, feedback: "This risks personal burnout and masks realistic planning capacity." }
    ]
  },
  {
    id: 3,
    pillar: 'internal',
    title: "Database Schema Expansion",
    context: "You need to add custom fields to our database to trace active model evaluations, but you aren't sure how it might impact the platform squad.",
    choices: [
      { id: 'A', text: "Apply the migration changes directly to staging to see if anything breaks during integration.", correct: false, feedback: "This can disrupt team efforts. Always seek collaboration before changing shared environments." },
      { id: 'B', text: "Implement the modifications silently and draft an automated alert informing developers after the fact.", correct: false, feedback: "This bypasses active consultation. Proactive alignment prevents issues." },
      { id: 'C', text: "Involve the platform and database engineers early to discuss constraints before proposing the schema update.", correct: true, feedback: "Superb. Involving stakeholders early instead of working in isolation builds internal trust." }
    ]
  },
  {
    id: 4,
    pillar: 'internal',
    title: "Model Threshold Disagreement",
    context: "A senior researcher asserts that the classification threshold should remain at 0.85. You have metrics showing 0.75 performs better on edge-case data.",
    choices: [
      { id: 'A', text: "Yield to their experience without showing your results, assuming seniority knows best.", correct: false, feedback: "Conceding without healthy discourse bypasses physical/virtual review peer feedback." },
      { id: 'B', text: "Present your metrics, false-positive curves, and logic in a shared doc to foster a constructive comparison.", correct: true, feedback: "Excellent! Using objective evidence and data to support your view supports healthy, respectful debate." },
      { id: 'C', text: "Challenge their threshold during a fast-paced sprint review, highlighting the choice as outdated.", correct: false, feedback: "Public challenges without objective preparation can lead to unnecessary defensiveness." }
    ]
  },
  {
    id: 5,
    pillar: 'internal',
    title: "UI Dashboard Redesign Conflict",
    context: "You disagree with the UI mockups for the new evaluation dashboard. You feel it hides crucial model metadata from developers.",
    choices: [
      { id: 'A', text: "Ask questions to understand the design choices, then explain the importance of the missing metadata.", correct: true, feedback: "Spot on. Questioning assumptions constructively before rejecting design concepts prevents friction." },
      { id: 'B', text: "Request that the frontend team rewrite the mockups because they 'clearly do not meet dev requirements.'", correct: false, feedback: "A dismissive approach can shut down collaboration. Focus on constructive suggestions." },
      { id: 'C', text: "Ignore the issue and build a custom CLI utility for your personal use instead.", correct: false, feedback: "Failing to collaborate on shared interfaces leads to fragmented tooling." }
    ]
  },
  {
    id: 6,
    pillar: 'internal',
    title: "Public PR Feedback Friction",
    context: "You notice structural performance bugs in a colleague's PR. You want to point it out without making them feel defensive.",
    choices: [
      { id: 'A', text: "Leave a comment: 'This code logic is highly inefficient and should be completely refactored.'", correct: false, feedback: "This focuses criticism on the developer's work rather than the idea or the performance itself." },
      { id: 'B', text: "Approve the PR anyway, then push a quick patch yourself later to fix the performance issue.", correct: false, feedback: "Bypassing constructive code review misses a chance to learn together." },
      { id: 'C', text: "State the performance issue objectively, suggest an alternative algorithm, and separate the code logic from the person.", correct: true, feedback: "Excellent. Separating the idea from the author builds trust and improves systemic output." }
    ]
  },
  {
    id: 7,
    pillar: 'internal',
    title: "Silent Developers in Retro",
    context: "During a retro, two outgoing developers dominate the conversation. Several junior members have remained silent the entire session.",
    choices: [
      { id: 'A', text: "Let the talk flow naturally, assuming quiet members will speak if they have concerns.", correct: false, feedback: "Ignoring silent members misses valuable ideas. Explicit inclusion is key." },
      { id: 'B', text: "Invite silent team members directly: 'Hey [Name], we'd love to hear your thoughts on this sprint if you have feedback.'", correct: true, feedback: "Perfect. Actively inviting contributions from those who haven't spoken creates room for every voice." },
      { id: 'C', text: "Wrap up the session early, since the loudest concerns have been resolved.", correct: false, feedback: "This neglects the shared retro framework and limits inclusive learning." }
    ]
  },
  {
    id: 8,
    pillar: 'internal',
    title: "The Written RFC Preference",
    context: "An introverted researcher prefers writing highly detailed RFCs over presenting design concepts in chaotic live meetings.",
    choices: [
      { id: 'A', text: "Demand they present live anyway to boost their verbal communication skills.", correct: false, feedback: "Forcing one style ignores natural strengths and preferences." },
      { id: 'B', text: "Allow asynchronous RFC review cycles first, so the team can digest the information before discussing.", correct: true, feedback: "Excellent. Being mindful of different communication styles enhances psychological safety." },
      { id: 'C', text: "Ignore the written RFCs and only prioritize decisions discussed in sync meetings.", correct: false, feedback: "This excludes valuable asynchronously prepared work." }
    ]
  },
  {
    id: 9,
    pillar: 'internal',
    title: "Stand-Up Over-Sharing",
    context: "You realize that during morning stand-ups, you tend to spend several minutes explaining minor technical implementation details.",
    choices: [
      { id: 'A', text: "Continue the deep dives, as it proves how hard you are working on complex tasks.", correct: false, feedback: "Dominating meetings with niche details reduces overall team focus." },
      { id: 'B', text: "Summarize high-level progress and blockers, offering to take deep dives offline.", correct: true, feedback: "Great self-awareness. Avoiding dominating discussions respects team time." },
      { id: 'C', text: "Stop sharing details altogether to keep your stand-up updates under ten seconds.", correct: false, feedback: "This swings too far, leaving the team without necessary context." }
    ]
  },
  {
    id: 10,
    pillar: 'internal',
    title: "Staging Pipeline Downtime",
    context: "An automated script you deployed ran into an edge case and crashed the team's shared staging deployment server.",
    choices: [
      { id: 'A', text: "Quietly fix the script, restart the server, and hope nobody noticed the brief downtime.", correct: false, feedback: "This misses an opportunity to learn openly and flags risk avoidance." },
      { id: 'B', text: "Post in Slack explaining the crash, why it happened, and what steps you've taken to prevent a recurrence.", correct: true, feedback: "Perfect. Learning openly and treating failures as collective lessons builds trust." },
      { id: 'C', text: "Blame the infrastructure tool for not catching the out-of-memory exception.", correct: false, feedback: "Defensiveness and blame shift attention away from root cause learning." }
    ]
  },
  {
    id: 11,
    pillar: 'internal',
    title: "Addressing a Missed Project Sprint",
    context: "The squad missed the sprint target due to unexpected integration challenges. Teammates are frustrated and pointing fingers.",
    choices: [
      { id: 'A', text: "Identify the developers who fell behind and reassign their modules to faster team members.", correct: false, feedback: "Blame-based adjustments harm morale and ignore root systemic constraints." },
      { id: 'B', text: "Run a retrospective focused on improving pipeline boundaries, not placing individual blame.", correct: true, feedback: "Exactly. Focusing retrospectives on improvement, not blame, builds psychological safety." },
      { id: 'C', text: "Cancel the sprint retrospective to avoid uncomfortable conversations.", correct: false, feedback: "Skipping retrospectives hides bottlenecks and hinders collective growth." }
    ]
  },
  {
    id: 12,
    pillar: 'internal',
    title: "An Experiment with Null Results",
    context: "You spent a week testing a new hyperparameter set, but the resulting model accuracy showed absolutely zero improvements.",
    choices: [
      { id: 'A', text: "Delete the branch and forget the project so the team thinks you were only working on successful tasks.", correct: false, feedback: "This wastes valuable technical context and lessons." },
      { id: 'B', text: "Write up a summary of the experiment, documenting the parameters tested and why it didn't work.", correct: true, feedback: "Excellent. Highlighting learnings over pure successes helps scale knowledge." },
      { id: 'C', text: "Manipulate the presentation charts to show a marginal, theoretical improvement.", correct: false, feedback: "This compromises scientific and technical integrity." }
    ]
  },
  {
    id: 13,
    pillar: 'internal',
    title: "Failed Custom Loss Function",
    context: "You designed a custom loss function that destabilized the training runs. You need to present your sprint update.",
    choices: [
      { id: 'A', text: "Discuss the destabilization issue openly, outlining the mathematical assumptions that failed.", correct: true, feedback: "Spot on. Sharing what didn't work saves other developers time and builds technical transparency." },
      { id: 'B', text: "Focus only on the successful training setups, omitting the custom loss function failure.", correct: false, feedback: "Hiding failures prevents the team from learning from technical pitfalls." },
      { id: 'C', text: "Say that 'external environment shifts' corrupted the training logs.", correct: false, feedback: "This violates our commitment to ownership and integrity." }
    ]
  },
  {
    id: 14,
    pillar: 'internal',
    title: "Handing Off the Vector Pipeline",
    context: "You finished building the custom vector embedding pipeline. You are about to move to another project.",
    choices: [
      { id: 'A', text: "Ping the incoming developer: 'Hey, the code is in main. It should be relatively straightforward.'", correct: false, feedback: "Vague handoffs lead to downstream confusion and system breakage." },
      { id: 'B', text: "Write a comprehensive README detailing schemas, deployment steps, and core mathematical trade-offs.", correct: true, feedback: "Perfect. Documenting knowledge ensures scale beyond single individuals." },
      { id: 'C', text: "Offer to hop on a quick call, assuming written notes are unnecessary.", correct: false, feedback: "Calls are helpful, but lack the persistent reference of documentation." }
    ]
  },
  {
    id: 15,
    pillar: 'internal',
    title: "Heuristic Data Cleaning Assumptions",
    context: "You used a statistical heuristic to remove 5% of outliers in our training data. It works well, but isn't explicitly mentioned in the code.",
    choices: [
      { id: 'A', text: "Document this cleaning assumption and its implications directly in the project's codebase.", correct: true, feedback: "Great. Capturing decisions and assumptions is vital for future troubleshooting." },
      { id: 'B', text: "Keep the heuristic as a secret% outlier removal to prove mathematical optimization.", correct: false, feedback: "Information hoarding hurts code quality and team resilience." },
      { id: 'C', text: "Wait until someone asks why the data shape changed before explaining the heuristic.", correct: false, feedback: "Reactive sharing causes confusion. Share assumptions proactively." }
    ]
  },
  {
    id: 16,
    pillar: 'internal',
    title: "Discovered an API Inefficiency",
    context: "While writing code, you notice a teammate's utility function performs redundant database queries.",
    choices: [
      { id: 'A', text: "Ignore it since it isn't part of your immediate sprint tasks.", correct: false, feedback: "Passive approaches to code quality limit collective growth." },
      { id: 'B', text: "Rewrite their code silently without telling them, assuming they won't mind.", correct: false, feedback: "Silent modifications can feel dismissive. Collaborate instead." },
      { id: 'C', text: "Share your optimization insight proactively, offering a simple suggested refactoring.", correct: true, feedback: "Excellent. Proactive sharing of insights scales quality and strengthens team capability." }
    ]
  },
  {
    id: 17,
    pillar: 'internal',
    title: "Modifying Shared Test Architectures",
    context: "You need to update our shared evaluation metrics script, which will impact several other active branches.",
    choices: [
      { id: 'A', text: "Merge the changes to main directly to keep things moving as fast as possible.", correct: false, feedback: "This risks breaking other branches without warning." },
      { id: 'B', text: "Propose the modifications in a shared channel, outline the impact, and ask for coordination.", correct: true, feedback: "Perfect. Coordinating across branches builds robust, collaborative software." },
      { id: 'C', text: "Create a separate, duplicated file, bypassing the shared script entirely.", correct: false, feedback: "Duplicating code leads to technical debt and fragmented tooling." }
    ]
  },

  // EXTERNAL PARTNERSHIPS (18-34)
  {
    id: 18,
    pillar: 'external',
    title: "Client-Facing Milestone Delays",
    context: "A critical external delivery is scheduled for Friday. On Tuesday, you realize integration issues will push it to Monday.",
    choices: [
      { id: 'A', text: "Wait until Friday afternoon to inform the client, hoping they won't check until next week.", correct: false, feedback: "Late-stage alerts damage client confidence. Early warnings are key." },
      { id: 'B', text: "Communicate the integration risks and new timeline on Tuesday, explaining the steps you are taking.", correct: true, feedback: "Exactly. Sharing risks and delays early demonstrates accountability and preserves trust." },
      { id: 'C', text: "Submit an incomplete milestone on Friday and quietly patch the bugs over the weekend.", correct: false, feedback: "Delivering compromised work risks client-side systems and harms integrity." }
    ]
  },
  {
    id: 19,
    pillar: 'external',
    title: "Client Asks for Performance Guarantees",
    context: "An external stakeholder demands a written guarantee that our new model will always maintain over 99% accuracy in production.",
    choices: [
      { id: 'A', text: "Sign the guarantee to secure the renewal, assuming we can address edge cases later.", correct: false, feedback: "Overpromising on ML metrics risks client trust when drift occurs." },
      { id: 'B', text: "Provide a direct explanation of data drift and set realistic expectations for performance.", correct: true, feedback: "Spot on. Prioritizing long-term trust and being honest about feasibility builds stronger relationships." },
      { id: 'C', text: "Avoid responding to their email, hoping they will forget the question.", correct: false, feedback: "Lack of communication degrades client relationships and trust." }
    ]
  },
  {
    id: 20,
    pillar: 'external',
    title: "Third-Party API Disruption",
    context: "A critical external data partner API is unstable, which will slow down the next project sprint.",
    choices: [
      { id: 'A', text: "Keep the issue internal until the client notices a performance drop in their portal.", correct: false, feedback: "Reactive updates can make clients feel left in the dark." },
      { id: 'B', text: "Notify the client of the partner's API status, explaining our mitigations and timeline.", correct: true, feedback: "Perfect. Informing stakeholders early helps manage expectations under changing conditions." },
      { id: 'C', text: "Cancel the project milestone and blame the third-party provider in a formal email.", correct: false, feedback: "Blame-shifting does not build partnership value." }
    ]
  },
  {
    id: 21,
    pillar: 'external',
    title: "Reporting Metric Discrepancies",
    context: "You discover a calculation error in a report delivered to a client yesterday. The revised accuracy is 1.5% lower.",
    choices: [
      { id: 'A', text: "Inform the client, provide the corrected metrics, and outline our mitigation steps.", correct: true, feedback: "Superb. Taking immediate ownership of mistakes is a core part of building long-term trust." },
      { id: 'B', text: "Keep silent, as a 1.5% change is too minor for the client to notice.", correct: false, feedback: "Concealing metrics harms our commitment to transparency." },
      { id: 'C', text: "Wait until the next quarterly review to slide the corrected charts into the presentation.", correct: false, feedback: "Delaying corrections can look like an attempt to hide mistakes." }
    ]
  },
  {
    id: 22,
    pillar: 'external',
    title: "Angry Client Accusations",
    context: "A client engineer blames our API integration for a database crash on their side, though our logs look normal.",
    choices: [
      { id: 'A', text: "Reply defensively, pointing out that their database setup is outdated.", correct: false, feedback: "Defensiveness can escalate tension. Stay calm and collaborative." },
      { id: 'B', text: "Suggest joint debugging sessions, remaining calm, respectful, and solution-focused.", correct: true, feedback: "Excellent. Handing difficult client discussions constructively builds partnership value." },
      { id: 'C', text: "Ignore their communication until they provide formal server logs.", correct: false, feedback: "This delay can hurt client-side operational flow." }
    ]
  },
  {
    id: 23,
    pillar: 'external',
    title: "Unrealistic Scoping Requests",
    context: "During a project kickoff, the client requests three custom evaluations that are outside our agreed contract.",
    choices: [
      { id: 'A', text: "Agree to their requests anyway to keep them happy, and worry about team capacity later.", correct: false, feedback: "This can lead to project delays and team burnout." },
      { id: 'B', text: "Outline the scope boundaries, prioritize their requests, and discuss budget or timeline adjustments.", correct: true, feedback: "Perfect. Aligning clearly on expectations from the start is essential." },
      { id: 'C', text: "Reject their requests flatly, citing the strict scope of work terms.", correct: false, feedback: "While boundary-setting is good, a dismissive approach can damage the relationship." }
    ]
  },
  {
    id: 24,
    pillar: 'external',
    title: "Client-Side Restructuring",
    context: "A sudden reorganization at our client's firm introduces a new sponsor who does not understand our technical value proposition.",
    choices: [
      { id: 'A', text: "Schedule a high-level review, translating our technical deliverables into business value metrics.", correct: true, feedback: "Excellent. Simplifying technical depth and adapting to the audience builds alignment." },
      { id: 'B', text: "Send them our technical API documentation and code repositories to review.", correct: false, feedback: "Flooding non-technical sponsors with raw code can increase confusion." },
      { id: 'C', text: "Continue delivering as usual, assuming the previous sponsor set the direction.", correct: false, feedback: "Failing to align with new leadership risks project support." }
    ]
  },
  {
    id: 25,
    pillar: 'external',
    title: "Dismissive Partner Conduct",
    context: "During a joint integration call, an external engineer makes a dismissive remark about our data structure.",
    choices: [
      { id: 'A', text: "Make a defensive comment to defend our technical setup.", correct: false, feedback: "Responding defensively can hinder collaboration." },
      { id: 'B', text: "Address their critique with objective metrics and keep the discussion constructively.", correct: true, feedback: "Great. Managing professional boundaries with respect keeps the focus on solutions." },
      { id: 'C', text: "Report their comment to their executive sponsor immediately.", correct: false, feedback: "This escalates minor friction unnecessarily. Resolve peer-to-peer first." }
    ]
  },
  {
    id: 26,
    pillar: 'external',
    title: "Explaining Latency to Business Leaders",
    context: "You need to explain a model latency spike of 200ms to a client's non-technical business leaders.",
    choices: [
      { id: 'A', text: "Use clear business terms: 'This latency increase means users may see a slight delay in results, but our accuracy is preserved.'", correct: true, feedback: "Perfect. Focusing on user impact rather than database internals helps simplify complexity." },
      { id: 'B', text: "Explain the latency spike in terms of multi-threading contention and database cache misses.", correct: false, feedback: "This relies on jargon that may confuse business leaders." },
      { id: 'C', text: "Provide a minimal summary that says: 'Model latency is within standard limits.'", correct: false, feedback: "Vague summaries can hide real performance changes." }
    ]
  },
  {
    id: 27,
    pillar: 'external',
    title: "Explaining Model Drift Risks",
    context: "A client's data has drifted, and their model accuracy is declining. You need to explain why retraining is necessary.",
    choices: [
      { id: 'A', text: "Explain: 'The real-world data has changed over time. Retraining is like updating a map to reflect new roads.'", correct: true, feedback: "Excellent. Using clear comparisons and analogies is a great way to simplify complexity." },
      { id: 'B', text: "Send a paper on covariate shift in high-dimensional feature spaces.", correct: false, feedback: "A technical paper may be too dense for business sponsors." },
      { id: 'C', text: "State that the model is performing exactly as designed and requires no changes.", correct: false, feedback: "This ignores the reality of data drift and client value." }
    ]
  },
  {
    id: 28,
    pillar: 'external',
    title: "Partner Insists on Outdated Libraries",
    context: "A key integration partner insists on using an outdated, insecure library for the database connector.",
    choices: [
      { id: 'A', text: "Agree to their request to keep the timeline on track.", correct: false, feedback: "Compromising security for speed risks long-term trust and system safety." },
      { id: 'B', text: "Highlight the security risks and recommend a modern, secure alternative.", correct: true, feedback: "Perfect. Recommending better alternatives over short-term gains builds trust." },
      { id: 'C', text: "Refuse to work with them until they update their entire infrastructure.", correct: false, feedback: "This can stall progress. Present constructive solutions instead." }
    ]
  },
  {
    id: 29,
    pillar: 'external',
    title: "Client Requests 48-Hour Model Build",
    context: "A client asks us to build a custom language model in 48 hours for an upcoming presentation.",
    choices: [
      { id: 'A', text: "Agree to the timeline, then deliver a generic template model to meet the date.", correct: false, feedback: "This compromises on our commitment to delivery standards." },
      { id: 'B', text: "Explain what is feasible in 48 hours and propose a realistic roadmap for a custom model.", correct: true, feedback: "Exactly. Being honest about feasibility protects long-term trust." },
      { id: 'C', text: "Inform them that their request is technically impossible and decline to help.", correct: false, feedback: "A blunt rejection misses a chance to guide the client constructively." }
    ]
  },
  {
    id: 30,
    pillar: 'external',
    title: "Discovered Model Pipeline Edge-Case Bias",
    context: "Under heavy deadline pressure, you find an edge-case bias in our pipeline that affects 1% of users.",
    choices: [
      { id: 'A', text: "Report the finding, outline the risk, and adjust the delivery timeline to patch the issue.", correct: true, feedback: "Superb. Prioritizing quality and fairness over short-term gains builds trust." },
      { id: 'B', text: "Ignore the edge case for now, as 1% is below our standard error threshold.", correct: false, feedback: "Ignoring bias issues can lead to systemic problems later." },
      { id: 'C', text: "Patch the code silently and deploy it without updating the release logs.", correct: false, feedback: "This lacks transparency and limits shared learning." }
    ]
  },
  {
    id: 31,
    pillar: 'external',
    title: "Client-Facing Deliverable Verification",
    context: "The client-facing model dashboard is ready for launch, but the team skipped the final verification tests due to a tight schedule.",
    choices: [
      { id: 'A', text: "Launch the dashboard on schedule, assuming any issues can be patched post-release.", correct: false, feedback: "Releasing unverified systems can damage trust if issues occur." },
      { id: 'B', text: "Postpone the launch briefly to run the final checks, explaining the value of these tests.", correct: true, feedback: "Perfect. We don't compromise quality or responsibility to move faster." },
      { id: 'C', text: "Deliver the code directly to their engineers and let them handle the verification.", correct: false, feedback: "This shifts our responsibility and ownership onto the client." }
    ]
  },
  { id: 32, pillar: 'external', title: "Aligning on Delivery Scope", context: "A client asks for several out-of-scope adjustments to a dashboard mid-project.", choices: [ { id: 'A', text: "Discuss the impact of these changes on our timeline and outline a clear path for future scoping.", correct: true, feedback: "Great. Set clear boundaries and maintain professionalism." }, { id: 'B', text: "Agree to all changes without adjusting our delivery timeline.", correct: false, feedback: "Overpromising risks quality and team well-being." }, { id: 'C', text: "Refuse the updates flatly and refer them to the contract terms.", correct: false, feedback: "A direct refusal can harm long-term collaboration." } ] },
  { id: 33, pillar: 'external', title: "Technical Presentation for Stakeholders", context: "You need to explain a complex model update to a client's non-technical team.", choices: [ { id: 'A', text: "Prepare a clear summary focusing on what this update means for their user experience.", correct: true, feedback: "Excellent. Simplifying complexity builds stronger partner relationships." }, { id: 'B', text: "Present the updated model architecture diagrams and parameter metrics.", correct: false, feedback: "This can overwhelm non-technical audiences." }, { id: 'C', text: "Delegate the presentation to a business manager without providing technical context.", correct: false, feedback: "This avoids our responsibility to translate technical depth." } ] },
  { id: 34, pillar: 'external', title: "Managing Project Scoping Shifts", context: "A sudden budget adjustment on the client side requires us to scale back our project deliverables.", choices: [ { id: 'A', text: "Work with the client to prioritize core deliverables and maintain quality on those items.", correct: true, feedback: "Perfect. Prioritize long-term trust and deliver value consistently." }, { id: 'B', text: "Reduce the quality of our testing across all deliverables to fit the new budget.", correct: false, feedback: "Compromising on quality to save costs risks long-term trust." }, { id: 'C', text: "Decline to adjust our project plans and insist on the original scope.", correct: false, feedback: "A rigid stance can lead to project cancellation." } ] },

  // LEADERSHIP AND ENABLING (35-50)
  {
    id: 35,
    pillar: 'leadership',
    title: "Junior Dev Deletes Staging Assets",
    context: "A junior developer accidentally deletes a critical bucket on our staging server during integration testing.",
    choices: [
      { id: 'A', text: "Remove their write access to prevent future operational mistakes.", correct: false, feedback: "This can damage confidence and ignores the root permissions setup." },
      { id: 'B', text: "Rebuild the assets together, normalize the mistake, and document better guardrails.", correct: true, feedback: "Perfect! Normalizing learning and responding positively when people share mistakes builds safety." },
      { id: 'C', text: "Deliver a formal warning about following staging guidelines.", correct: false, feedback: "A punitive approach can discourage future transparency." }
    ]
  },
  {
    id: 36,
    pillar: 'leadership',
    title: "Teammate Admits Lack of Framework Knowledge",
    context: "A high-performing developer admits in confidence that they feel out of their depth with our new orchestration engine.",
    choices: [
      { id: 'A', text: "Reassign their orchestration tasks to someone with more experience.", correct: false, feedback: "This can look like a penalty and limits their chance to grow." },
      { id: 'B', text: "Validate their honesty, share your own experiences with new tools, and allocate training time.", correct: true, feedback: "Excellent. Normalizing uncertainty and supporting growth builds a resilient team." },
      { id: 'C', text: "Tell them to study the documentation in their personal time to catch up.", correct: false, feedback: "Shifting training entirely to personal time can lead to burnout." }
    ]
  },
  {
    id: 37,
    pillar: 'leadership',
    title: "Addressing Interruptions in Planning",
    context: "During a planning meeting, a senior engineer interrupts a junior colleague who is proposing an alternative approach.",
    choices: [
      { id: 'A', text: "Intervene constructively: 'I'd love to hear [Name] finish their thought first, then we can look at alternatives.'", correct: true, feedback: "Perfect. Addressing dismissive behavior early helps maintain psychological safety." },
      { id: 'B', text: "Let it pass to keep the meeting on schedule and avoid any team friction.", correct: false, feedback: "Passivity in the face of interruptions can erode team safety." },
      { id: 'C', text: "Reprimand the senior developer publicly in front of the entire team.", correct: false, feedback: "A public reprimand can create defensive dynamics." }
    ]
  },
  {
    id: 38,
    pillar: 'leadership',
    title: "Manager Miscomputes Project Estimate",
    context: "As a team lead, you realize your project timeline estimate was off by two weeks, which will impact our roadmap.",
    choices: [
      { id: 'A', text: "Admit the planning error openly, adjust the roadmap, and discuss resource adjustments with the team.", correct: true, feedback: "Excellent. Leading by example means being accountable for our own decisions." },
      { id: 'B', text: "Ask the team to work overtime to make up for the estimation error.", correct: false, feedback: "This shifts the burden of a management error onto team well-being." },
      { id: 'C', text: "Blame the delays on unexpected technical challenges in our database connector.", correct: false, feedback: "This shifts accountability away from management decisions." }
    ]
  },
  {
    id: 39,
    pillar: 'leadership',
    title: "Company Pivot Causes Team Anxiety",
    context: "A sudden shift in company goals leaves your team feeling uncertain about the future of their projects.",
    choices: [
      { id: 'A', text: "Avoid discussing the pivot until we have absolute clarity from executive sponsors.", correct: false, feedback: "Silence during pivots can increase team anxiety." },
      { id: 'B', text: "Organize a team sync to discuss the pivot, share what you know, and outline our priorities.", correct: true, feedback: "Perfect. Leading with transparency during uncertainty helps align and support the team." },
      { id: 'C', text: "Tell the team that everything is fine and discourage questions about the pivot.", correct: false, feedback: "This can erode trust and ignores team concerns." }
    ]
  },
  {
    id: 40,
    pillar: 'leadership',
    title: "Late-Night Server Outage Responsibility",
    context: "A database outage occurs at 10 PM. As the technical lead, you realize you missed a warning in the logs earlier that day.",
    choices: [
      { id: 'A', text: "Help resolve the outage, take responsibility for the oversight, and update our monitoring alerts.", correct: true, feedback: "Superb. Showing accountability and focusing on system solutions builds team trust." },
      { id: 'B', text: "Blame the on-call engineer for not catching the database crash sooner.", correct: false, feedback: "Blaming others ignores our responsibility to lead by example." },
      { id: 'C', text: "Say that the database hosting provider suffered an unpreventable outage.", correct: false, feedback: "This avoids our commitment to operational integrity." }
    ]
  },
  {
    id: 41,
    pillar: 'leadership',
    title: "Teammate Proposes testing Unsupervised Frameworks",
    context: "An engineer wants to spend 10% of their sprint cycle testing a new unsupervised framework that might optimize our pipeline.",
    choices: [
      { id: 'A', text: "Support the experiment, define clear success metrics, and review the results together.", correct: true, feedback: "Exactly. Supporting space for learning and exploration is a core value." },
      { id: 'B', text: "Decline the request, citing the importance of our immediate sprint tasks.", correct: false, feedback: "This can discourage team initiative and technical curiosity." },
      { id: 'C', text: "Tell them they can run the test if they make up the sprint hours over the weekend.", correct: false, feedback: "This approach to exploration risks team burnout." }
    ]
  },
  {
    id: 42,
    pillar: 'leadership',
    title: "Junior Dev Proposes a Hackathon Project",
    context: "A junior developer proposes a custom hackathon project to optimize our internal dataset pipelines.",
    choices: [
      { id: 'A', text: "Encourage their initiative, help them refine their pitch, and connect them with a senior mentor.", correct: true, feedback: "Perfect. Enabling growth and supporting team initiative is essential." },
      { id: 'B', text: "Advise them to focus on simpler tasks until they have more engineering experience.", correct: false, feedback: "This can stifle growth and limit professional initiative." },
      { id: 'C', text: "Tell them to wait until our next annual hackathon to explore the idea.", correct: false, feedback: "Delaying support can discourage team curiosity." }
    ]
  },
  {
    id: 43,
    pillar: 'leadership',
    title: "Developer Wants to Attend ML Conference",
    context: "A developer wants to attend a major ML conference that does not immediately align with their sprint tasks.",
    choices: [
      { id: 'A', text: "Approve the request, and ask them to share their key takeaways with the team afterward.", correct: true, feedback: "Great. Supporting learning beyond immediate tasks builds long-term capability." },
      { id: 'B', text: "Decline the request, as the conference does not directly support their current sprint.", correct: false, feedback: "This limits opportunities for professional growth and innovation." },
      { id: 'C', text: "Deduct the conference days from their personal paid time off balance.", correct: false, feedback: "Treating professional training as personal leave can harm retention." }
    ]
  },
  {
    id: 44,
    pillar: 'leadership',
    title: "Explaining sudden Strategy Changes",
    context: "A sudden corporate pivot requires your team to stop working on a project they have spent weeks building.",
    choices: [
      { id: 'A', text: "Explain the strategic reasons behind the pivot and discuss how our work can support the new goals.", correct: true, feedback: "Perfect. Explaining the 'why' behind decisions helps align and motivate the team." },
      { id: 'B', text: "Instruct the team to stop work immediately, without explaining the decision.", correct: false, feedback: "Leaving teams in the dark can harm morale and commitment." },
      { id: 'C', text: "Blame the pivot on senior management decisions to distance yourself from the choice.", correct: false, feedback: "This can undermine team alignment and trust in leadership." }
    ]
  },
  {
    id: 45,
    pillar: 'leadership',
    title: "Teammate Blocked by Vague User Stories",
    context: "A developer feels blocked because our project requirements are vague, leading to several sprint adjustments.",
    choices: [
      { id: 'A', text: "Organize a requirements review, clarify the goals, and document clear acceptance criteria.", correct: true, feedback: "Excellent. Providing clarity and reducing ambiguity helps unblock the team." },
      { id: 'B', text: "Tell them to make their best assumptions and continue writing code anyway.", correct: false, feedback: "This can lead to rework and team frustration." },
      { id: 'C', text: "Blame the product manager publicly for the vague requirements.", correct: false, feedback: "This shifts accountability and can damage cross-team collaboration." }
    ]
  },
  {
    id: 46,
    pillar: 'leadership',
    title: "Handling Multiple High-Priority Tasks",
    context: "Your team is feeling overwhelmed by several competing high-priority tasks and shifting project deadlines.",
    choices: [
      { id: 'A', text: "Align with stakeholders, prioritize the core tasks, and clarify the delivery roadmap.", correct: true, feedback: "Exactly. Helping teams navigate priorities and trade-offs reduces burnout." },
      { id: 'B', text: "Instruct the team to work faster to deliver all tasks on schedule.", correct: false, feedback: "This approach to project delivery can lead to burnout." },
      { id: 'C', text: "Let the team decide what to prioritize, without providing coordination.", correct: false, feedback: "This can lead to fragmented efforts and delayed deliverables." }
    ]
  },
  {
    id: 47,
    pillar: 'leadership',
    title: "Protecting Late-Night Contributors",
    context: "You notice a high-performing developer is consistently committing code changes after 11 PM.",
    choices: [
      { id: 'A', text: "Organize a workload review, encourage healthier boundaries, and adjust their tasks if needed.", correct: true, feedback: "Excellent. Active support for sustainable pacing is key to team well-being." },
      { id: 'B', text: "Praise their late-night commits publicly to motivate other team members.", correct: false, feedback: "Praising long hours can promote an unsustainable work culture." },
      { id: 'C', text: "Ignore their hours, as long as they continue to deliver on-time updates.", correct: false, feedback: "Neglecting work hours can lead to team burnout." }
    ]
  },
  {
    id: 48,
    pillar: 'leadership',
    title: "Pushing Back Against Unrealistic Deadlines",
    context: "A business sponsor requests a project delivery date that your team estimates is two weeks too short.",
    choices: [
      { id: 'A', text: "Agree to the timeline, and ask the team to work extra hours to meet the date.", correct: false, feedback: "This can compromise project quality and team well-being." },
      { id: 'B', text: "Present a realistic timeline, outline the quality risks of a rushed launch, and discuss a phased delivery.", correct: true, feedback: "Perfect. Protecting sustainable performance and being honest about timelines builds trust." },
      { id: 'C', text: "Accept the deadline and reduce our QA testing steps to meet the date.", correct: false, feedback: "This compromises project quality and system stability." }
    ]
  },
  {
    id: 49,
    pillar: 'leadership',
    title: "Sensing Burnout in a High-Performer",
    context: "A reliable teammate has become unusually quiet in meetings and missed several minor daily updates.",
    choices: [
      { id: 'A', text: "Schedule a supportive check-in, discuss their workload, and prioritize their well-being.", correct: true, feedback: "Perfect. Active monitoring of workload and team well-being is key to sustainable performance." },
      { id: 'B', text: "Send a reminder about the importance of our daily stand-up updates.", correct: false, feedback: "Focusing only on tasks can miss underlying signs of burnout." },
      { id: 'C', text: "Wait until their mid-year performance review to discuss their engagement level.", correct: false, feedback: "Delaying support can allow burnout to impact well-being." }
    ]
  },
  {
    id: 50,
    pillar: 'leadership',
    title: "Giving Code Architecture Feedback",
    context: "An engineer's code is functional but does not follow our architectural standards. You need to give feedback.",
    choices: [
      { id: 'A', text: "Schedule a supportive 1:1, walk through the code together, and offer constructive refactoring suggestions.", correct: true, feedback: "Perfect. Giving constructive, actionable feedback in 1:1s supports professional growth." },
      { id: 'B', text: "Rewrite their code yourself and merge it without explaining the changes.", correct: false, feedback: "Bypassing feedback misses an opportunity for professional development." },
      { id: 'C', text: "Point out the architectural issues publicly in a team Slack channel.", correct: false, feedback: "Public criticism can undermine psychological safety." }
    ]
  }
];

export default function App() {
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'internal', 'external', 'leadership'
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPrinciple, setSelectedPrinciple] = useState(null);
  const [viewMode, setViewMode] = useState('dashboard'); // 'dashboard', 'onepager'
  const [copiedText, setCopiedText] = useState(null);

  // Scenarios State
  const [selectedPillarFilter, setSelectedPillarFilter] = useState('all');
  const [selectedStatusFilter, setSelectedStatusFilter] = useState('all');
  const [gymSearchQuery, setGymSearchQuery] = useState('');
  const [activeGymIndex, setActiveGymIndex] = useState(0);
  const [scenarioAttempts, setScenarioAttempts] = useState({}); // { scenarioId: { selectedId, correct } }

  // Upgraded AI Alignment Assessment Tool State
  const [assessmentMode, setAssessmentMode] = useState('challenge'); // 'custom', 'challenge'
  const [selectedChallengeIndex, setSelectedChallengeIndex] = useState(0);
  const [userSolution, setUserSolution] = useState('');
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [isAssessing, setIsAssessing] = useState(false);
  const [assessmentError, setAssessmentError] = useState(null);

  const [savedReflections, setSavedReflections] = useState([
    {
      date: 'Yesterday',
      text: 'Encouraged a quiet team member to share their thoughts during our design retro. Felt like a solid execution of "creating space for every voice".',
      overallScore: 92,
      feedback: 'Excellent alignment! By inviting input from those who haven\'t spoken, you directly built psychological safety and internal trust.'
    }
  ]);

  // AI Feature States
  const [aiSubTab, setAiSubTab] = useState('gym'); // 'gym', 'coach', 'simplifier', 'roleplay'

  // 1. AI Culture Coach State
  const [coachInput, setCoachInput] = useState('');
  const [coachResponse, setCoachResponse] = useState(null);
  const [isCoachLoading, setIsCoachLoading] = useState(false);
  const [coachError, setCoachError] = useState(null);

  // 2. AI Simplifier State
  const [simplifierInput, setSimplifierInput] = useState('');
  const [simplifierResponse, setSimplifierResponse] = useState(null);
  const [isSimplifierLoading, setIsSimplifierLoading] = useState(false);
  const [simplifierError, setSimplifierError] = useState(null);

  // 3. AI Dynamic Roleplay State
  const [roleplayPillar, setRoleplayPillar] = useState('internal');
  const [dynamicScenario, setDynamicScenario] = useState(null);
  const [dynamicSelection, setDynamicSelection] = useState(null);
  const [isRoleplayLoading, setIsRoleplayLoading] = useState(false);
  const [roleplayError, setRoleplayError] = useState(null);

  // Filtering Gym Scenarios
  const filteredGymScenarios = useMemo(() => {
    return SCENARIO_GYM_LIST.filter(scenario => {
      // Filter by Pillar
      if (selectedPillarFilter !== 'all' && scenario.pillar !== selectedPillarFilter) {
        return false;
      }

      // Filter by Completion Status
      const attempt = scenarioAttempts[scenario.id];
      if (selectedStatusFilter === 'correct') {
        if (!attempt || !attempt.correct) return false;
      } else if (selectedStatusFilter === 'incorrect') {
        if (!attempt || attempt.correct) return false;
      } else if (selectedStatusFilter === 'unattempted') {
        if (attempt) return false;
      }

      // Filter by Search Query
      if (gymSearchQuery.trim() !== '') {
        const query = gymSearchQuery.toLowerCase();
        const matchesTitle = scenario.title.toLowerCase().includes(query);
        const matchesContext = scenario.context.toLowerCase().includes(query);
        if (!matchesTitle && !matchesContext) return false;
      }

      return true;
    });
  }, [selectedPillarFilter, selectedStatusFilter, gymSearchQuery, scenarioAttempts]);

  // Dynamic active scenario within filtered list
  const activeGymScenario = useMemo(() => {
    if (filteredGymScenarios.length === 0) return null;
    const index = activeGymIndex % filteredGymScenarios.length;
    return filteredGymScenarios[index] || filteredGymScenarios[0];
  }, [filteredGymScenarios, activeGymIndex]);

  // Track achievements
  const gymStats = useMemo(() => {
    const total = SCENARIO_GYM_LIST.length;
    const completed = Object.keys(scenarioAttempts).length;
    const correct = Object.values(scenarioAttempts).filter(a => a.correct).length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    return { total, completed, correct, percentage };
  }, [scenarioAttempts]);

  // Handle Gym submission
  const handleGymSelect = (scenarioId, choice) => {
    setScenarioAttempts(prev => ({
      ...prev,
      [scenarioId]: {
        selectedId: choice.id,
        correct: choice.correct
      }
    }));
  };

  // Backoff helper to fetch from Gemini API
  const fetchGemini = async (promptText, systemText = PLAYBOOK_CONTEXT_PROMPT) => {
    const apiKey = ""; // API key injected at runtime
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;

    const payload = {
      contents: [
        {
          parts: [{ text: promptText }]
        }
      ],
      systemInstruction: {
        parts: [{ text: systemText }]
      },
      generationConfig: {
        responseMimeType: "application/json"
      }
    };

    const delays = [1000, 2000, 4000, 8000, 16000];
    let lastError = null;

    for (let attempt = 0; attempt <= 5; attempt++) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();
        const outputText = data.candidates?.[0]?.content?.parts?.[0]?.text;

        if (outputText) {
          return outputText;
        } else {
          throw new Error("Malformed API response structure.");
        }
      } catch (err) {
        lastError = err;
        if (attempt < 5) {
          await new Promise(res => setTimeout(res, delays[attempt]));
        }
      }
    }
    throw lastError || new Error("Connection failed after max backoff retries.");
  };

  // Triggering the AI Culture Coach
  const handleAskCoach = async (suggestedText = null) => {
    const query = suggestedText || coachInput;
    if (!query.trim()) return;

    setIsCoachLoading(true);
    setCoachError(null);
    setCoachResponse(null);

    const prompt = `
      I am facing this real-world workplace situation:
      "${query}"

      Analyze this situation against the official Iris.ai Culture Playbook guidelines. Give your structured response in JSON format matching the schema:
      {
        "corePrinciples": "Principles at stake...",
        "advice": "Actionable advice bullet points...",
        "slackMessage": "Drafted Slack/Email communication template..."
      }
    `;

    try {
      const responseText = await fetchGemini(prompt);
      const parsed = JSON.parse(responseText);
      const formatted = `### 🎯 Core Principles at Stake\n${parsed.corePrinciples}\n\n### 💡 Actionable Advice\n${parsed.advice}\n\n### ✨ Draft Slack/Email Message\n\`\`\`text\n${parsed.slackMessage}\n\`\`\``;
      setCoachResponse(formatted);
    } catch (err) {
      setCoachError("Our Culture Coach is temporarily offline. Please check your connection and try again.");
    } finally {
      setIsCoachLoading(false);
    }
  };

  // Triggering the AI Complexity Simplifier
  const handleAskSimplifier = async (suggestedText = null) => {
    const query = suggestedText || simplifierInput;
    if (!query.trim()) return;

    setIsSimplifierLoading(true);
    setSimplifierError(null);
    setSimplifierResponse(null);

    const prompt = `
      Please take this complex technical statement or jargon:
      "${query}"

      Apply the "We simplify complexity" Iris.ai principle. Return JSON matching:
      {
        "jargonBreakdown": "Underlying simple breakdown of the technology...",
        "clientFacing": "Translation for non-technical clients...",
        "whatMeansForYou": "Actionable implications and risk overview...",
        "analogy": "Clear analogy..."
      }
    `;

    try {
      const responseText = await fetchGemini(prompt);
      const parsed = JSON.parse(responseText);
      const formatted = `### 💡 Core Jargon Breakdown\n${parsed.jargonBreakdown}\n\n### 🗣️ Client-Facing Translation\n${parsed.clientFacing}\n\n### 🔑 "What You Need to Know / What This Means For You" Summary\n${parsed.whatMeansForYou}\n\n### 🎨 Analogy/Visual Comparison\n${parsed.analogy}`;
      setSimplifierResponse(formatted);
    } catch (err) {
      setSimplifierError("Complexity Simplifier encountered an error. Please try again.");
    } finally {
      setIsSimplifierLoading(false);
    }
  };

  // Generating a Dynamic Roleplay Challenge
  const handleGenerateRoleplay = async () => {
    setIsRoleplayLoading(true);
    setRoleplayError(null);
    setDynamicScenario(null);
    setDynamicSelection(null);

    const prompt = `
      Generate a realistic, challenging workplace dilemma scenario that focuses on the Iris.ai pillar: "${roleplayPillar.toUpperCase()}".

      Respond STRICTLY in the following raw JSON format:
      {
        "context": "A description of the high-stakes situation...",
        "choices": [
          {
            "id": "A",
            "text": "Option A approach...",
            "feedback": "Why this approach is perfect, good, or misses key playbook concepts like...",
            "correct": true
          },
          {
            "id": "B",
            "text": "Option B approach...",
            "feedback": "Why this approach fails or compromises trust, quality, etc...",
            "correct": false
          },
          {
            "id": "C",
            "text": "Option C approach...",
            "feedback": "Why this is mediocre or ignores active inclusion...",
            "correct": false
          }
        ]
      }
    `;

    try {
      const rawText = await fetchGemini(prompt);
      const parsed = JSON.parse(rawText);
      setDynamicScenario(parsed);
    } catch (err) {
      setRoleplayError("Could not generate a dynamic roleplay at this moment. Please retry.");
    } finally {
      setIsRoleplayLoading(false);
    }
  };

  // Triggering the upgraded AI Alignment Assessment grading
  const handleEvaluateAlignment = async () => {
    if (!userSolution.trim()) return;
    setIsAssessing(true);
    setAssessmentError(null);
    setAssessmentResult(null);

    const dilemmaContext = assessmentMode === 'challenge'
      ? ASSESSMENT_CHALLENGES[selectedChallengeIndex].context
      : "Custom daily workplace reflection entry";

    const prompt = `
      You are evaluating a team member's response/solution to a workplace dilemma based strictly on the Iris.ai Culture Playbook.

      Workplace dilemma/context: "${dilemmaContext}"
      Team member's response/solution: "${userSolution}"

      Grade their solution out of 100 on absolute alignment with Iris.ai values. Detail their grade scores out of 5 for each of the 3 playbook pillars:
      - Internal Collaboration (openness, respect, blameless learning, space for voices)
      - External Partnerships (ownership, transparent risk warnings, simplify technical complexity, commitments)
      - Leadership & Enabling (psychological safety, leading by example, sustainable performance)

      Be constructive and objective. Provide the output in valid, structured JSON format with this exact schema:
      {
        "overallScore": 85, // out of 100
        "internalScore": 4, // integer score out of 5
        "externalScore": 5, // integer score out of 5
        "leadershipScore": 3, // integer score out of 5
        "keyPillarFollowed": "Which specific Iris.ai principle did they apply best...",
        "assessmentExplanation": "Constructive analysis of their response explaining why it aligns or how it conflicts...",
        "correctiveRecommendation": "A tailored actionable recommendation to improve compliance even further..."
      }
    `;

    try {
      const responseText = await fetchGemini(prompt);
      const parsed = JSON.parse(responseText);
      setAssessmentResult(parsed);
    } catch (err) {
      setAssessmentError("AI Assessment engine was unable to grade your answer. Please review your response and try again.");
    } finally {
      setIsAssessing(false);
    }
  };

  // Log evaluated scorecard into historical record
  const handleSaveScorecard = () => {
    if (!assessmentResult) return;
    const challengeTitle = assessmentMode === 'challenge'
      ? ASSESSMENT_CHALLENGES[selectedChallengeIndex].title
      : "Real Daily Work";

    const newScorecard = {
      date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      text: `[${challengeTitle}] Answer: ${userSolution}`,
      overallScore: assessmentResult.overallScore,
      feedback: `AI feedback: ${assessmentResult.keyPillarFollowed}. ${assessmentResult.assessmentExplanation}`
    };

    setSavedReflections([newScorecard, ...savedReflections]);
    setUserSolution('');
    setAssessmentResult(null);
  };

  // Clipboard copy helper
  const handleCopy = (text, label) => {
    const tempInput = document.createElement('textarea');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    setCopiedText(label);
    setTimeout(() => setCopiedText(null), 2000);
  };

  // Filter logic
  const filteredData = useMemo(() => {
    let result = { ...PLAYBOOK_DATA };

    if (activeTab !== 'all') {
      const keys = Object.keys(result);
      keys.forEach(key => {
        if (key !== activeTab) delete result[key];
      });
    }

    if (searchQuery.trim() !== '') {
      const query = searchQuery.toLowerCase();
      const searchSection = (section) => {
        return {
          ...section,
          principles: section.principles.filter(p =>
            p.title.toLowerCase().includes(query) ||
            p.desc.toLowerCase().includes(query) ||
            p.practices.some(prac => prac.toLowerCase().includes(query)) ||
            p.triggers.some(trig => trig.toLowerCase().includes(query))
          )
        };
      };

      const keys = Object.keys(result);
      keys.forEach(key => {
        const filteredSection = searchSection(result[key]);
        if (filteredSection.principles.length > 0) {
          result[key] = filteredSection;
        } else {
          delete result[key];
        }
      });
    }

    return result;
  }, [activeTab, searchQuery]);

  const totalMatches = useMemo(() => {
    return Object.values(filteredData).reduce((sum, sec) => sum + (sec.principles ? sec.principles.length : 0), 0);
  }, [filteredData]);

  return (
    <div className="min-h-screen bg-[#030614] text-slate-100 font-sans antialiased selection:bg-[#7F4F9F] selection:text-white pb-16 print:bg-white print:text-black">

      {/* Background Orbs */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-[#3C49CC]/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute top-[800px] right-10 w-[400px] h-[400px] bg-[#7F4F9F]/10 rounded-full blur-[100px] pointer-events-none" />

      {/* Top Header Banner */}
      <header className="border-b border-slate-800 bg-[#030614]/80 backdrop-blur sticky top-0 z-50 transition-all duration-300 print:hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">

          {/* Typographic Badge Header with 'The Iris.ai Way' */}
          <div className="flex items-center gap-3">
            <a href="https://iris.ai/" target="_blank" rel="noopener noreferrer" className="relative px-3 py-1.5 rounded-lg bg-[#3C49CC]/10 border border-[#3C49CC]/30 flex items-center justify-center shadow-lg shadow-[#3C49CC]/20 hover:opacity-90 transition-all duration-300">
              <span className="font-sans font-extrabold text-sm tracking-wide text-white flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-blue-400" />
                Iris.ai
              </span>
            </a>
            <div>
              <a href="https://iris.ai/" target="_blank" rel="noopener noreferrer" className="hover:opacity-80 transition block">
                <span className="font-bold text-lg tracking-wider text-white block">
                  The Iris.ai Way
                </span>
                <span className="text-[10px] tracking-widest uppercase text-[#E2E1F3]/60 block -mt-1 font-medium">Culture Hub</span>
              </a>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-1">
              <button
                onClick={() => setViewMode('dashboard')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-semibold tracking-wide transition-all ${viewMode === 'dashboard' ? 'bg-[#3C49CC] text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
              >
                <Compass className="w-3.5 h-3.5" />
                Interactive App
              </button>
              <button
                onClick={() => setViewMode('onepager')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-semibold tracking-wide transition-all ${viewMode === 'onepager' ? 'bg-[#7F4F9F] text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
              >
                <Printer className="w-3.5 h-3.5" />
                One-Pager Poster
              </button>
            </div>

            <button
              onClick={() => window.print()}
              className="bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white p-2 rounded-lg border border-slate-700 transition"
              title="Print Culture Playbook"
            >
              <Printer className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Grid container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">

        {/* Playbook Hero */}
        {viewMode === 'dashboard' && (
          <div className="mb-10 p-8 rounded-2xl bg-gradient-to-r from-slate-950 via-[#030614] to-slate-950 border border-slate-800/80 shadow-2xl relative overflow-hidden print:hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-[#7F4F9F]/10 to-[#3C49CC]/10 rounded-full blur-3xl" />
            <div className="max-w-3xl">
              <span className="inline-flex items-center gap-1.5 bg-[#3C49CC]/10 border border-[#3C49CC]/40 text-blue-400 px-3 py-1 rounded-full text-xs font-semibold tracking-wider uppercase mb-4">
                <Sparkles className="w-3.5 h-3.5" />
                The Iris.ai Way
              </span>
              <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2 flex items-center gap-2.5">
                Your Culture Playbook
              </h1>
              <p className="text-base text-slate-300 leading-relaxed mb-6">
                This playbook is not about following rules — it's about making thoughtful choices in how you work with others. Our goal is not just to do great work, but to create an environment where great work can happen consistently.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-slate-800 pt-6">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-[#3C49CC]/20 flex items-center justify-center text-[#3C49CC]">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Internal Trust</h4>
                    <p className="text-[11px] text-slate-400">Openness & shared ownership</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-[#7F4F9F]/20 flex items-center justify-center text-[#7F4F9F]">
                    <ExternalLink className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">External Integrity</h4>
                    <p className="text-[11px] text-slate-400">Accountability & clarity</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-400">
                    <Zap className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Lead & Enable</h4>
                    <p className="text-[11px] text-slate-400">Psychological safety & growth</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ----------------- MODE A: INTERACTIVE DASHBOARD ----------------- */}
        {viewMode === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 print:hidden">

            {/* Left Column containing principles list & Search */}
            <div className="lg:col-span-8 space-y-8">

              {/* ✨ INTRODUCING THE GEMINI AI & GYM COMPANION SUITE ✨ */}
              <div className="p-6 rounded-2xl bg-gradient-to-b from-[#0b0f24] to-[#040716] border-2 border-[#3C49CC]/40 shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-[#7F4F9F]/20 rounded-full blur-2xl pointer-events-none" />

                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-4">
                  <div className="flex items-center gap-2.5">
                    <div className="w-10 h-10 rounded-xl bg-[#3C49CC]/20 flex items-center justify-center text-[#3C49CC]">
                      <Sparkles className="w-5 h-5 text-indigo-400 animate-pulse" />
                    </div>
                    <div>
                      <h2 className="text-base font-extrabold text-white flex items-center gap-1.5">
                        Playbook Action Hub
                      </h2>
                      <p className="text-xs text-slate-400">Master the values through 50 interactive exercises & AI-driven feedback</p>
                    </div>
                  </div>

                  {/* Internal Navigation for Action Hub */}
                  <div className="flex flex-wrap bg-slate-950 p-1 rounded-lg border border-slate-850 gap-1">
                    <button
                      onClick={() => setAiSubTab('gym')}
                      className={`px-3 py-1 rounded text-xs font-bold transition ${aiSubTab === 'gym' ? 'bg-[#3C49CC] text-white' : 'text-slate-400 hover:text-slate-200'}`}
                    >
                      50 Scenario Gym 💪
                    </button>
                    <button
                      onClick={() => setAiSubTab('coach')}
                      className={`px-3 py-1 rounded text-xs font-bold transition ${aiSubTab === 'coach' ? 'bg-[#7F4F9F] text-white' : 'text-slate-400 hover:text-slate-200'}`}
                    >
                      AI Culture Coach ✨
                    </button>
                    <button
                      onClick={() => setAiSubTab('simplifier')}
                      className={`px-3 py-1 rounded text-xs font-bold transition ${aiSubTab === 'simplifier' ? 'bg-[#3C49CC]/80 text-white' : 'text-slate-400 hover:text-slate-200'}`}
                    >
                      AI Jargon Simplifier ✨
                    </button>
                    <button
                      onClick={() => setAiSubTab('roleplay')}
                      className={`px-3 py-1 rounded text-xs font-bold transition ${aiSubTab === 'roleplay' ? 'bg-emerald-600 text-white' : 'text-slate-400 hover:text-slate-200'}`}
                    >
                      AI Roleplay Generator ✨
                    </button>
                  </div>
                </div>

                {/* Tab 0 Content: 50 Scenarios Gym */}
                {aiSubTab === 'gym' && (
                  <div className="space-y-6">
                    {/* Progress & Header */}
                    <div className="bg-slate-950 p-4 rounded-xl border border-slate-850/80">
                      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-3">
                        <div>
                          <h3 className="text-xs font-black uppercase text-slate-300 flex items-center gap-1.5">
                            <Award className="w-4 h-4 text-[#7F4F9F]" />
                            Playbook Mastery Progress
                          </h3>
                          <p className="text-[11px] text-slate-500">Solve situations across Internal, External, and Leadership guidelines</p>
                        </div>
                        <div className="text-right">
                          <span className="text-xs font-extrabold text-[#3C49CC]">
                            {gymStats.correct} / {gymStats.total} Correct
                          </span>
                          <span className="text-[10px] text-slate-500 block">({gymStats.percentage}% Completed)</span>
                        </div>
                      </div>

                      {/* Progress Bar */}
                      <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800/60">
                        <div
                          className="bg-gradient-to-r from-[#3C49CC] via-[#7F4F9F] to-emerald-500 h-full transition-all duration-500"
                          style={{ width: `${gymStats.percentage}%` }}
                        />
                      </div>
                    </div>

                    {/* Filter controls */}
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div>
                        <label className="text-[9px] uppercase font-bold text-slate-500 block mb-1">Pillar filter</label>
                        <select
                          value={selectedPillarFilter}
                          onChange={(e) => { setSelectedPillarFilter(e.target.value); setActiveGymIndex(0); }}
                          className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-300 focus:outline-none focus:ring-1 focus:ring-[#3C49CC]"
                        >
                          <option value="all">All Pillars</option>
                          <option value="internal">1. Internal Collaboration</option>
                          <option value="external">2. External Partnering</option>
                          <option value="leadership">3. Leadership & Enabling</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-[9px] uppercase font-bold text-slate-500 block mb-1">Status filter</label>
                        <select
                          value={selectedStatusFilter}
                          onChange={(e) => { setSelectedStatusFilter(e.target.value); setActiveGymIndex(0); }}
                          className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-300 focus:outline-none focus:ring-1 focus:ring-[#3C49CC]"
                        >
                          <option value="all">All States</option>
                          <option value="unattempted">Unattempted</option>
                          <option value="correct">Correct</option>
                          <option value="incorrect">Incorrect</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-[9px] uppercase font-bold text-slate-500 block mb-1">Search Exercises</label>
                        <input
                          type="text"
                          value={gymSearchQuery}
                          onChange={(e) => { setGymSearchQuery(e.target.value); setActiveGymIndex(0); }}
                          placeholder="Search scenario context..."
                          className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-300 focus:outline-none focus:ring-1 focus:ring-[#3C49CC] placeholder-slate-600"
                        />
                      </div>
                    </div>

                    {/* Scenario Presenter */}
                    {activeGymScenario ? (
                      <div className="bg-slate-950 p-5 rounded-xl border border-slate-800 relative space-y-4">
                        <div className="flex justify-between items-start gap-3 border-b border-slate-900 pb-3">
                          <div>
                            <span className="text-[9px] bg-[#3C49CC]/20 border border-[#3C49CC]/40 text-blue-400 px-2 py-0.5 rounded font-black tracking-widest uppercase">
                              Scenario {activeGymScenario.id} — {activeGymScenario.pillar}
                            </span>
                            <h4 className="text-sm font-bold text-white mt-1.5">{activeGymScenario.title}</h4>
                          </div>

                          <span className="text-xs text-slate-500 font-bold">
                            {activeGymIndex + 1} of {filteredGymScenarios.length} matches
                          </span>
                        </div>

                        <p className="text-xs text-slate-200 leading-relaxed bg-slate-900/40 p-3.5 rounded-lg border border-slate-850 italic">
                          "{activeGymScenario.context}"
                        </p>

                        {/* Choices */}
                        <div className="space-y-2.5">
                          {activeGymScenario.choices.map((choice) => {
                            const attempt = scenarioAttempts[activeGymScenario.id];
                            const isSelected = attempt?.selectedId === choice.id;

                            let choiceStyle = "bg-slate-900 border-slate-800 hover:border-slate-700 text-slate-300";
                            if (isSelected) {
                              choiceStyle = choice.correct
                                ? "bg-emerald-950/40 border-emerald-500 text-emerald-200"
                                : "bg-rose-950/40 border-rose-500 text-rose-200";
                            } else if (attempt && choice.correct) {
                              // Highlight correct answer if attempted
                              choiceStyle = "bg-slate-900/60 border-emerald-500/30 text-emerald-300/80";
                            }

                            return (
                              <button
                                key={choice.id}
                                onClick={() => handleGymSelect(activeGymScenario.id, choice)}
                                className={`w-full text-left p-3 rounded-lg text-xs transition border flex items-start gap-2.5 ${choiceStyle}`}
                              >
                                <span className="font-bold text-[10px] text-slate-500 mt-0.5 uppercase">Option {choice.id}:</span>
                                <span>{choice.text}</span>
                              </button>
                            );
                          })}
                        </div>

                        {/* Feedback Banner */}
                        {scenarioAttempts[activeGymScenario.id] && (
                          <div className={`p-4 rounded-xl border text-xs leading-relaxed ${
                            scenarioAttempts[activeGymScenario.id].correct
                              ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300'
                              : 'bg-rose-950/20 border-rose-500/40 text-rose-300'
                          }`}>
                            <div className="font-bold flex items-center gap-1.5 mb-1">
                              {scenarioAttempts[activeGymScenario.id].correct ? (
                                <CheckCircle className="w-4 h-4 text-emerald-400" />
                              ) : (
                                <AlertCircle className="w-4 h-4 text-rose-400" />
                              )}
                              {scenarioAttempts[activeGymScenario.id].correct ? 'Perfect Choice!' : 'Room for improvement'}
                            </div>
                            <p>{activeGymScenario.choices.find(c => c.id === scenarioAttempts[activeGymScenario.id].selectedId)?.feedback}</p>
                          </div>
                        )}

                        {/* Pagination */}
                        <div className="flex justify-between items-center pt-3 border-t border-slate-900">
                          <button
                            onClick={() => {
                              setActiveGymIndex((prev) => (prev > 0 ? prev - 1 : filteredGymScenarios.length - 1));
                            }}
                            className="text-xs font-semibold text-slate-400 hover:text-white transition"
                          >
                            ← Previous
                          </button>

                          <button
                            onClick={() => {
                              setActiveGymIndex((prev) => (prev + 1) % filteredGymScenarios.length);
                            }}
                            className="bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold px-4 py-1.5 rounded-lg transition"
                          >
                            Next Exercise →
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div className="text-center py-12 bg-slate-950 border border-slate-850 rounded-xl">
                        <Info className="w-8 h-8 text-slate-600 mx-auto mb-2" />
                        <p className="text-xs text-slate-400">No exercises found matching your current filters.</p>
                        <button
                          onClick={() => { setSelectedPillarFilter('all'); setSelectedStatusFilter('all'); setGymSearchQuery(''); }}
                          className="mt-3 bg-[#3C49CC] text-white text-[11px] font-bold px-3 py-1.5 rounded-lg"
                        >
                          Clear Filters
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* Tab 1 Content: AI Culture Coach */}
                {aiSubTab === 'coach' && (
                  <div className="space-y-4">
                    <p className="text-xs text-slate-300">
                      Got a tricky situation? Ask the AI Coach how to resolve it according to Iris.ai values (Internal trust, client feedback, or workload boundary stress).
                    </p>
                    <div className="flex flex-col gap-2">
                      <textarea
                        value={coachInput}
                        onChange={(e) => setCoachInput(e.target.value)}
                        placeholder="E.g., A client is pushing us to release a model early without doing subgroup bias checks. How do I say no while retaining trust?"
                        rows="3"
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-[#3C49CC] placeholder-slate-500"
                      />

                      {/* Suggestion tags to stimulate usage */}
                      <div className="flex flex-wrap gap-2 items-center">
                        <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">Try Suggestions:</span>
                        {[
                          "Teammate dominates discussions",
                          "Handling code testing vs Friday deadlines",
                          "Addressing immediate signs of team burnout"
                        ].map((sug, i) => (
                          <button
                            key={i}
                            onClick={() => {
                              setCoachInput(sug);
                              handleAskCoach(sug);
                            }}
                            className="bg-slate-950 hover:bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 px-2 py-1 rounded text-[10px]"
                          >
                            {sug}
                          </button>
                        ))}
                      </div>

                      <div className="flex justify-between items-center pt-2">
                        {coachError && (
                          <div className="flex items-center gap-1.5 text-xs text-rose-400">
                            <AlertCircle className="w-3.5 h-3.5" />
                            <span>{coachError}</span>
                          </div>
                        )}
                        <span />
                        <button
                          onClick={() => handleAskCoach()}
                          disabled={isCoachLoading || !coachInput.trim()}
                          className="bg-gradient-to-r from-[#3C49CC] to-[#7F4F9F] hover:opacity-90 disabled:opacity-50 text-white font-bold text-xs px-4 py-2 rounded-xl flex items-center gap-1.5 transition ml-auto"
                        >
                          {isCoachLoading ? (
                            <>
                              <Loader2 className="w-3.5 h-3.5 animate-spin" />
                              Analyzing Playbook...
                            </>
                          ) : (
                            <>
                              <Sparkles className="w-3.5 h-3.5" />
                              Get Coaching Advice ✨
                            </>
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Coach Response Panel */}
                    {coachResponse && (
                      <div className="mt-4 bg-slate-950/90 border border-[#3C49CC]/30 rounded-xl p-4 space-y-4 max-h-96 overflow-y-auto">
                        <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                          <span className="text-xs font-bold text-indigo-400 flex items-center gap-1.5">
                            <CheckCircle className="w-4 h-4 text-emerald-400" />
                            Playbook Coach Alignment Results
                          </span>
                          <button
                            onClick={() => handleCopy(coachResponse, "coach_copy")}
                            className="text-xs text-slate-400 hover:text-white flex items-center gap-1"
                          >
                            {copiedText === "coach_copy" ? (
                              <span className="text-emerald-400 font-bold text-[11px]">Copied Advice!</span>
                            ) : (
                              <>
                                <Copy className="w-3.5 h-3.5" />
                                Copy Output
                              </>
                            )}
                          </button>
                        </div>
                        <div className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap prose prose-invert">
                          {coachResponse}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Tab 2 Content: Technical Jargon Translators */}
                {aiSubTab === 'simplifier' && (
                  <div className="space-y-4">
                    <p className="text-xs text-slate-300">
                      Iris.ai rule: **"We simplify complexity. Focus on what it means, not just how it works."** Paste your extreme deep-learning jargon here to transform it into clean stakeholder value.
                    </p>
                    <div className="flex flex-col gap-2">
                      <textarea
                        value={simplifierInput}
                        onChange={(e) => setSimplifierInput(e.target.value)}
                        placeholder="E.g., The anisotropic embeddings in the vector database suffer from severe cosine metric degradation due to out-of-distribution drift."
                        rows="3"
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-[#7F4F9F] placeholder-slate-500"
                      />

                      <div className="flex flex-wrap gap-2 items-center">
                        <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">Try Jargon Examples:</span>
                        {[
                          "Anisotropic embeddings suffer cosine drift",
                          "High multi-collinearity in XGBoost outputs",
                          "Quantization losses in float16 to int8 inference"
                        ].map((sug, i) => (
                          <button
                            key={i}
                            onClick={() => {
                              setSimplifierInput(sug);
                              handleAskSimplifier(sug);
                            }}
                            className="bg-slate-950 hover:bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 px-2 py-1 rounded text-[10px]"
                          >
                            {sug}
                          </button>
                        ))}
                      </div>

                      <div className="flex justify-between items-center pt-2">
                        {simplifierError && (
                          <div className="flex items-center gap-1.5 text-xs text-rose-400">
                            <AlertCircle className="w-3.5 h-3.5" />
                            <span>{simplifierError}</span>
                          </div>
                        )}
                        <span />
                        <button
                          onClick={() => handleAskSimplifier()}
                          disabled={isSimplifierLoading || !simplifierInput.trim()}
                          className="bg-gradient-to-r from-[#7F4F9F] to-indigo-700 hover:opacity-90 disabled:opacity-50 text-white font-bold text-xs px-4 py-2 rounded-xl flex items-center gap-1.5 transition ml-auto"
                        >
                          {isSimplifierLoading ? (
                            <>
                              <Loader2 className="w-3.5 h-3.5 animate-spin" />
                              Simplifying Technical Depth...
                            </>
                          ) : (
                            <>
                              <Sparkles className="w-3.5 h-3.5" />
                              Simplify Jargon ✨
                            </>
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Simplifier Response Output */}
                    {simplifierResponse && (
                      <div className="mt-4 bg-slate-950/90 border border-[#7F4F9F]/30 rounded-xl p-4 space-y-4 max-h-96 overflow-y-auto">
                        <div className="flex justify-between items-center border-b border-slate-800 pb-2">
                          <span className="text-xs font-bold text-purple-400 flex items-center gap-1.5">
                            <CheckCircle className="w-4 h-4 text-emerald-400" />
                            Simplified Communications Translation
                          </span>
                          <button
                            onClick={() => handleCopy(simplifierResponse, "simplifier_copy")}
                            className="text-xs text-slate-400 hover:text-white flex items-center gap-1"
                          >
                            {copiedText === "simplifier_copy" ? (
                              <span className="text-emerald-400 font-bold text-[11px]">Copied Translation!</span>
                            ) : (
                              <>
                                <Copy className="w-3.5 h-3.5" />
                                Copy Translation
                              </>
                            )}
                          </button>
                        </div>
                        <div className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap prose prose-invert">
                          {simplifierResponse}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Tab 3 Content: Dynamic LLM Roleplay Challenge Generator */}
                {aiSubTab === 'roleplay' && (
                  <div className="space-y-4">
                    <p className="text-xs text-slate-300">
                      Generate an endless supply of interactive scenarios based directly on the playbook. Challenge yourself and get real-time feedback on your judgment.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 items-center bg-slate-950 p-4 rounded-xl border border-slate-850">
                      <div className="flex flex-col gap-1 w-full sm:w-1/2">
                        <label className="text-[10px] text-slate-400 uppercase tracking-widest font-bold">Select Pillar of Practice</label>
                        <select
                          value={roleplayPillar}
                          onChange={(e) => setRoleplayPillar(e.target.value)}
                          className="bg-slate-900 border border-slate-800 rounded-lg py-1.5 px-3 text-xs text-slate-200 focus:ring-1 focus:ring-indigo-500"
                        >
                          <option value="internal">1. Internal Collaboration</option>
                          <option value="external">2. External Partnerships</option>
                          <option value="leadership">3. Leadership and Enabling</option>
                        </select>
                      </div>

                      <button
                        onClick={handleGenerateRoleplay}
                        disabled={isRoleplayLoading}
                        className="w-full sm:w-auto mt-4 sm:mt-0 ml-auto bg-gradient-to-r from-emerald-600 to-indigo-700 hover:opacity-90 disabled:opacity-50 text-white font-bold text-xs px-5 py-3 rounded-xl flex items-center justify-center gap-1.5 transition"
                      >
                        {isRoleplayLoading ? (
                          <>
                            <Loader2 className="w-3.5 h-3.5 animate-spin" />
                            Constructing Scenario...
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-3.5 h-3.5" />
                            Generate Custom Scenario ✨
                          </>
                        )}
                      </button>
                    </div>

                    {roleplayError && (
                      <div className="flex items-center gap-1.5 text-xs text-rose-400 bg-rose-950/20 p-3 rounded-lg border border-rose-900/50">
                        <AlertCircle className="w-4 h-4" />
                        <span>{roleplayError}</span>
                      </div>
                    )}

                    {/* Dynamic Scenario display */}
                    {dynamicScenario && (
                      <div className="space-y-4 bg-slate-950 p-5 rounded-xl border border-emerald-900/30">
                        <div className="space-y-1">
                          <span className="text-[9px] bg-emerald-950 border border-emerald-500/40 text-emerald-400 px-2 py-0.5 rounded uppercase font-bold tracking-widest">
                            Dynamic Challenge
                          </span>
                          <p className="text-xs text-slate-200 leading-relaxed font-semibold pt-1">
                            "{dynamicScenario.context}"
                          </p>
                        </div>

                        <div className="space-y-2">
                          {dynamicScenario.choices?.map((choice, i) => (
                            <button
                              key={i}
                              onClick={() => setDynamicSelection(choice)}
                              className={`w-full text-left p-3.5 rounded-xl text-xs transition border flex items-start gap-3 ${
                                dynamicSelection?.id === choice.id
                                ? (choice.correct ? 'bg-emerald-950/40 border-emerald-500 text-emerald-200' : 'bg-rose-950/40 border-rose-500 text-rose-200')
                                : 'bg-slate-900/60 border-slate-800/80 hover:bg-slate-900 hover:border-slate-700 text-slate-300'
                              }`}
                            >
                              <span className="font-black text-slate-500 uppercase mt-0.5 shrink-0">Option {choice.id}:</span>
                              <span>{choice.text}</span>
                            </button>
                          ))}
                        </div>

                        {dynamicSelection && (
                          <div className={`p-4 rounded-xl border text-xs leading-relaxed ${dynamicSelection.correct ? 'bg-emerald-950/20 border-emerald-500/40 text-emerald-300' : 'bg-rose-950/20 border-rose-500/40 text-rose-300'}`}>
                            <div className="font-bold flex items-center gap-1.5 mb-1.5">
                              {dynamicSelection.correct ? <CheckCircle className="w-4 h-4 text-emerald-400" /> : <AlertCircle className="w-4 h-4 text-rose-400" />}
                              {dynamicSelection.correct ? "Aligned Choice!" : "Room for alignment"}
                            </div>
                            <p>{dynamicSelection.feedback}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Standard Filter and Search Bar */}
              <div className="flex flex-col sm:flex-row gap-4 justify-between items-center bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                <div className="flex flex-wrap gap-2 w-full sm:w-auto">
                  {[
                    { id: 'all', label: 'All Principles' },
                    { id: 'internal', label: '1. Internal Collaboration' },
                    { id: 'external', label: '2. External Partners' },
                    { id: 'leadership', label: '3. Leadership' }
                  ].map(tab => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${activeTab === tab.id ? 'bg-[#3C49CC] text-white shadow-md' : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'}`}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>

                <div className="relative w-full sm:w-64">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-slate-500">
                    <Search className="w-4 h-4" />
                  </span>
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search triggers & values..."
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg py-1.5 pl-10 pr-4 text-xs focus:outline-none focus:ring-2 focus:ring-[#3C49CC] text-slate-200 placeholder-slate-500"
                  />
                  {searchQuery && (
                    <button
                      onClick={() => setSearchQuery('')}
                      className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] uppercase font-bold text-slate-500 hover:text-white"
                    >
                      Clear
                    </button>
                  )}
                </div>
              </div>

              {/* No Results Fallback */}
              {totalMatches === 0 && (
                <div className="text-center py-16 bg-slate-900/20 border border-dashed border-slate-800 rounded-2xl">
                  <Info className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                  <p className="text-slate-400 font-semibold mb-1">No cultural guidelines match your search.</p>
                  <p className="text-xs text-slate-500 max-w-sm mx-auto">Try searching generic keywords like "burnout", "documentation", or "client".</p>
                  <button
                    onClick={() => { setSearchQuery(''); setActiveTab('all'); }}
                    className="mt-4 bg-[#3C49CC] hover:bg-blue-600 text-white text-xs font-semibold px-4 py-2 rounded-lg transition"
                  >
                    Reset Filters
                  </button>
                </div>
              )}

              {/* Loop through filtered categories */}
              {Object.entries(filteredData).map(([sectionKey, section]) => (
                <div key={sectionKey} className="space-y-4">

                  {/* Section Title Header */}
                  <div className="flex items-center gap-3 border-b border-slate-800/60 pb-3">
                    <div className={`p-2 rounded-lg bg-gradient-to-tr ${section.color} text-white`}>
                      {sectionKey === 'internal' && <Users className="w-5 h-5" />}
                      {sectionKey === 'external' && <ExternalLink className="w-5 h-5" />}
                      {sectionKey === 'leadership' && <Compass className="w-5 h-5" />}
                    </div>
                    <div>
                      <h2 className="text-lg font-bold tracking-tight text-white">{section.title}</h2>
                      <p className="text-xs text-slate-400">{section.subtitle}</p>
                    </div>
                  </div>

                  {/* Principle Cards Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {section.principles.map((p) => (
                      <div
                        key={p.id}
                        onClick={() => setSelectedPrinciple(p)}
                        className={`group relative text-left p-5 rounded-xl border transition-all duration-300 cursor-pointer bg-gradient-to-br from-slate-950 to-[#030614] hover:to-slate-900/40 ${selectedPrinciple?.id === p.id ? 'border-[#3C49CC] ring-1 ring-[#3C49CC]/30' : 'border-slate-800/80 hover:border-slate-700'}`}
                      >
                        <div className="flex justify-between items-start gap-4 mb-2">
                          <h3 className="text-sm font-bold text-white group-hover:text-blue-400 transition">
                            {p.title}
                          </h3>
                          <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-slate-400 transition shrink-0 mt-0.5" />
                        </div>
                        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
                          {p.desc}
                        </p>

                        {/* Dynamic Tags Preview */}
                        <div className="flex flex-wrap gap-1.5">
                          {p.triggers.slice(0, 2).map((trig, idx) => (
                            <span key={idx} className="bg-slate-900 text-slate-400 px-2 py-0.5 rounded text-[10px] font-medium border border-slate-800/50">
                              {trig}
                            </span>
                          ))}
                          {p.triggers.length > 2 && (
                            <span className="text-slate-500 text-[9px] font-bold self-center">
                              +{p.triggers.length - 2} more
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}

            </div>

            {/* Right Interactive Sidebar Pane */}
            <div className="lg:col-span-4 space-y-8">

              {/* Upgraded AI Alignment Assessment Tool */}
              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
                <div className="flex items-center gap-2">
                  <div className="bg-emerald-500/20 text-emerald-400 p-1.5 rounded-lg">
                    <Heart className="w-4 h-4 animate-pulse" />
                  </div>
                  <div>
                    <h3 className="text-xs font-extrabold text-white uppercase tracking-wider">AI Alignment Assessment</h3>
                    <p className="text-[10px] text-slate-500">Objective grading against Culture Principles</p>
                  </div>
                </div>

                {/* Mode Toggler */}
                <div className="grid grid-cols-2 gap-2 bg-slate-950 p-1 rounded-lg border border-slate-805">
                  <button
                    type="button"
                    onClick={() => {
                      setAssessmentMode('custom');
                      setUserSolution('');
                      setAssessmentResult(null);
                      setAssessmentError(null);
                    }}
                    className={`py-1 rounded text-[10px] font-bold transition ${assessmentMode === 'custom' ? 'bg-[#3C49CC] text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
                  >
                    Analyze My Work
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setAssessmentMode('challenge');
                      setUserSolution('');
                      setAssessmentResult(null);
                      setAssessmentError(null);
                    }}
                    className={`py-1 rounded text-[10px] font-bold transition ${assessmentMode === 'challenge' ? 'bg-[#7F4F9F] text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
                  >
                    Solve AI Dilemma
                  </button>
                </div>

                {/* Sub-inputs based on state */}
                {assessmentMode === 'challenge' ? (
                  <div className="space-y-2">
                    <label className="text-[9px] uppercase font-bold text-slate-500 block">Select playbook scenario</label>
                    <select
                      value={selectedChallengeIndex}
                      onChange={(e) => {
                        setSelectedChallengeIndex(parseInt(e.target.value));
                        setUserSolution('');
                        setAssessmentResult(null);
                        setAssessmentError(null);
                      }}
                      className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 text-xs text-slate-300 focus:outline-none focus:ring-1 focus:ring-[#7F4F9F]"
                    >
                      {ASSESSMENT_CHALLENGES.map((ch, idx) => (
                        <option key={idx} value={idx}>{ch.title}</option>
                      ))}
                    </select>
                    <div className="bg-slate-950/80 p-3.5 rounded-lg border border-slate-850 text-xs text-slate-300 leading-relaxed italic">
                      "{ASSESSMENT_CHALLENGES[selectedChallengeIndex].context}"
                    </div>
                  </div>
                ) : (
                  <div className="bg-slate-950/40 p-3.5 rounded-lg border border-slate-850 text-xs text-slate-400 leading-relaxed">
                    Describe a workplace challenge or action item you encountered today. Our AI evaluation engine will audit and grade your solution on our simplified 1 to 5 scale.
                  </div>
                )}

                {/* Solution Input area */}
                <div className="space-y-2">
                  <label className="text-[9px] uppercase font-bold text-slate-500 block">Your solution / action plan</label>
                  <textarea
                    value={userSolution}
                    onChange={(e) => setUserSolution(e.target.value)}
                    placeholder={
                      assessmentMode === 'challenge'
                        ? "Describe how you'd resolve this, respecting sustainable performance or proactive clarity..."
                        : "Describe the situation and your exact response..."
                    }
                    rows="3"
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-[#3C49CC]"
                  />
                </div>

                {/* Action buttons */}
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={handleEvaluateAlignment}
                    disabled={isAssessing || !userSolution.trim()}
                    className="flex-1 bg-gradient-to-r from-[#3C49CC] to-[#7F4F9F] hover:opacity-90 disabled:opacity-50 text-white text-xs font-bold py-2 rounded-lg flex items-center justify-center gap-1.5 transition-all duration-300"
                  >
                    {isAssessing ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        Evaluating Solution...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-3.5 h-3.5 animate-pulse" />
                        Evaluate Alignment ✨
                      </>
                    )}
                  </button>

                  {assessmentResult && (
                    <button
                      type="button"
                      onClick={handleSaveScorecard}
                      className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold px-3 py-2 rounded-lg transition"
                      title="Save alignment score to your record"
                    >
                      Save
                    </button>
                  )}
                </div>

                {assessmentError && (
                  <div className="text-rose-400 text-xs flex items-center gap-1.5 bg-rose-950/20 p-2.5 rounded-lg border border-rose-900/40">
                    <AlertCircle className="w-3.5 h-3.5" />
                    <span>{assessmentError}</span>
                  </div>
                )}

                {/* Score Report Display */}
                {assessmentResult && (
                  <div className="bg-slate-950 border border-[#3C49CC]/40 rounded-xl p-4 space-y-4 animate-fadeIn">
                    <div className="flex justify-between items-center border-b border-slate-900 pb-2">
                      <span className="text-xs font-bold text-slate-300">Alignment Scorecard</span>
                      <span className="bg-[#3C49CC]/20 border border-[#3C49CC]/40 text-blue-400 text-xs font-extrabold px-2.5 py-0.5 rounded-full">
                        Score: {assessmentResult.overallScore}/5
                      </span>
                    </div>

                    {/* Breakdown by Pillars */}
                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div className="bg-slate-900 p-2 rounded-lg border border-slate-850">
                        <span className="text-[9px] uppercase font-bold text-slate-500 block">Internal</span>
                        <span className="text-xs font-extrabold text-blue-400">{assessmentResult.internalScore}/5</span>
                      </div>
                      <div className="bg-slate-900 p-2 rounded-lg border border-slate-850">
                        <span className="text-[9px] uppercase font-bold text-slate-500 block">External</span>
                        <span className="text-xs font-extrabold text-purple-400">{assessmentResult.externalScore}/5</span>
                      </div>
                      <div className="bg-slate-900 p-2 rounded-lg border border-slate-850">
                        <span className="text-[9px] uppercase font-bold text-slate-500 block">Leadership</span>
                        <span className="text-xs font-extrabold text-emerald-400">{assessmentResult.leadershipScore}/5</span>
                      </div>
                    </div>

                    <div className="space-y-1">
                      <span className="text-[9px] uppercase font-bold text-slate-500 tracking-widest block">Core Principle Used</span>
                      <p className="text-[11px] font-bold text-slate-200">{assessmentResult.keyPillarFollowed}</p>
                    </div>

                    <div className="space-y-1 text-xs text-slate-300">
                      <span className="text-[9px] uppercase font-bold text-slate-500 tracking-widest block">AI Feedback Analysis</span>
                      <p className="italic leading-relaxed">"{assessmentResult.assessmentExplanation}"</p>
                    </div>

                    {assessmentResult.correctiveRecommendation && (
                      <div className="bg-[#3C49CC]/10 border-l-2 border-[#3C49CC] pl-2.5 py-1.5 text-[11px] text-slate-400 leading-relaxed">
                        <span className="font-bold text-slate-200 block mb-0.5 text-[10px] uppercase">How to Align Closer</span>
                        <p>{assessmentResult.correctiveRecommendation}</p>
                      </div>
                    )}
                  </div>
                )}

                {/* Past Reflections & Score History List */}
                {savedReflections.length > 0 && (
                  <div className="pt-4 border-t border-slate-800/80 space-y-2.5">
                    <h4 className="text-[10px] uppercase font-bold tracking-widest text-slate-400">Scorecard & Reflection History</h4>
                    <div className="space-y-2 max-h-40 overflow-y-auto pr-1">
                      {savedReflections.map((ref, idx) => (
                        <div key={idx} className="bg-slate-950 p-2.5 rounded border border-slate-800 text-[11px] space-y-1.5">
                          <div className="flex justify-between items-center text-slate-400">
                            <span className="font-semibold text-slate-500">{ref.date}</span>
                            <div className="flex gap-1.5 font-extrabold text-[10px]">
                              {ref.overallScore ? (
                                <span className="text-blue-400">Align: {ref.overallScore}/5</span>
                              ) : (
                                <>
                                  <span className="text-[#3C49CC]">{ref.ratings?.internal}</span>
                                  <span className="text-[#7F4F9F]">{ref.ratings?.external}</span>
                                  <span className="text-emerald-400">{ref.ratings?.leadership}</span>
                                </>
                              )}
                            </div>
                          </div>
                          <p className="text-slate-300 leading-relaxed italic line-clamp-3">"{ref.text}"</p>
                          {ref.feedback && (
                            <div className="mt-1 bg-[#3C49CC]/5 border-l border-[#7F4F9F] pl-2 py-1 text-[10px] text-slate-400 leading-relaxed">
                              <p className="italic line-clamp-3">"{ref.feedback}"</p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Sidebar Detail Inspector Panel */}
              <div className="bg-slate-900/40 border border-slate-800 rounded-2xl p-6 sticky top-24 shadow-xl">
                {selectedPrinciple ? (
                  <div className="space-y-6">
                    <div className="flex justify-between items-start gap-2">
                      <span className="text-[10px] font-bold uppercase tracking-widest text-[#3C49CC] bg-[#3C49CC]/10 border border-[#3C49CC]/30 px-2 py-0.5 rounded">
                        Detailed Guideline
                      </span>
                      <button
                        onClick={() => setSelectedPrinciple(null)}
                        className="text-slate-500 hover:text-white text-xs font-semibold"
                      >
                        Deselect
                      </button>
                    </div>

                    <div>
                      <h3 className="text-base font-extrabold text-white mb-2">{selectedPrinciple.title}</h3>
                      <p className="text-xs text-slate-300 leading-relaxed italic">{selectedPrinciple.desc}</p>
                    </div>

                    <div className="space-y-3">
                      <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-400" />
                        What this means in practice
                      </h4>
                      <ul className="space-y-2">
                        {selectedPrinciple.practices.map((prac, i) => (
                          <li key={i} className="text-xs text-slate-400 flex items-start gap-2">
                            <span className="text-blue-500 mt-1 shrink-0">•</span>
                            <span>{prac}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="space-y-3 pt-3 border-t border-slate-800/80">
                      <h4 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                        <Zap className="w-3.5 h-3.5 text-[#7F4F9F]" />
                        When it matters most
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {selectedPrinciple.triggers.map((trig, i) => (
                          <span key={i} className="bg-slate-950 text-slate-300 px-2.5 py-1 rounded-md text-[11px] border border-slate-800 font-medium">
                            {trig}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Show example templates if present */}
                    {selectedPrinciple.example && (
                      <div className="pt-3 border-t border-slate-800/80 space-y-2">
                        <span className="text-[10px] font-extrabold text-[#7F4F9F] uppercase tracking-wider block">Playbook Blueprint</span>
                        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 relative">
                          <p className="text-xs italic text-slate-300 pr-6">
                            "{selectedPrinciple.example.text || selectedPrinciple.example.good}"
                          </p>
                          <button
                            onClick={() => handleCopy(selectedPrinciple.example.text || selectedPrinciple.example.good, selectedPrinciple.id)}
                            className="absolute right-2 top-2 text-slate-500 hover:text-white"
                          >
                            {copiedText === selectedPrinciple.id ? <span className="text-[9px] text-emerald-400 font-bold">Copied</span> : <Copy className="w-3 h-3" />}
                          </button>
                        </div>
                      </div>
                    )}

                  </div>
                ) : (
                  <div className="text-center py-10 space-y-4">
                    <div className="w-12 h-12 rounded-full bg-slate-950 border border-slate-800 flex items-center justify-center mx-auto text-slate-500">
                      <BookMarked className="w-5 h-5 animate-pulse" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-white">Interactive Inspector</h4>
                      <p className="text-xs text-slate-500 mt-1 max-w-xs mx-auto">
                        Click on any principle card to examine practical workflows, triggers, and communication blueprints.
                      </p>
                    </div>
                  </div>
                )}
              </div>

            </div>

          </div>
        )}

        {/* ----------------- MODE B: ONE-PAGER PRINTABLE POSTER ----------------- */}
        {viewMode === 'onepager' && (
          <div className="bg-[#030614] border border-slate-800 p-8 rounded-2xl shadow-2xl space-y-8 print:border-0 print:p-0 print:bg-white print:text-black">

            {/* Poster Header */}
            <div className="text-center pb-6 border-b border-slate-800">
              <div className="flex items-center justify-center gap-3 mb-2">
                <a href="https://iris.ai/" target="_blank" rel="noopener noreferrer" className="w-12 h-12 rounded-full bg-gradient-to-tr from-[#3C49CC] to-[#7F4F9F] flex items-center justify-center text-white font-black text-sm shadow-md">
                  Iris
                </a>
                <h1 className="text-3xl font-extrabold tracking-tight text-white print:text-black">
                  The <span className="text-[#3C49CC] print:text-blue-700">Iris.ai Way</span> Culture Playbook
                </h1>
              </div>
              <p className="text-sm text-slate-300 print:text-slate-600 max-w-2xl mx-auto leading-relaxed">
                "Not about following rules — it's about making thoughtful choices in how you work with others to create an environment where great work happens consistently."
              </p>
            </div>

            {/* Poster Grid - 3 Core Columns */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

              {/* Column 1: Internal Collaboration */}
              <div className="bg-slate-950/60 p-5 rounded-xl border border-slate-800/80 print:bg-slate-50 print:border-slate-300 space-y-4">
                <div className="border-b border-slate-800 pb-2 mb-2">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="w-2.5 h-2.5 rounded-full bg-[#3C49CC]" />
                    <h2 className="text-sm font-black uppercase tracking-wider text-white print:text-black">1. Internal Collaboration</h2>
                  </div>
                  <p className="text-[11px] text-slate-400 print:text-slate-600">
                    We build trust through openness, respect, and shared ownership.
                  </p>
                </div>

                <div className="space-y-4">
                  {PLAYBOOK_DATA.internal.principles.map((p, idx) => (
                    <div key={p.id} className="space-y-1.5">
                      <div className="flex gap-2 items-start">
                        <span className="text-[#3C49CC] font-bold text-xs">{idx + 1}.</span>
                        <h3 className="text-xs font-bold text-white print:text-black leading-tight">
                          {p.title}
                        </h3>
                      </div>
                      <p className="text-[10px] text-slate-400 print:text-slate-600 pl-4 leading-relaxed italic">
                        {p.desc}
                      </p>
                      <ul className="pl-4 space-y-1">
                        {p.practices.map((prac, i) => (
                          <li key={i} className="text-[10px] text-slate-300 print:text-slate-700 flex items-start gap-1">
                            <span className="text-[#3C49CC]/80 shrink-0">•</span>
                            <span>{prac}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>

              {/* Column 2: External Partnership */}
              <div className="bg-slate-950/60 p-5 rounded-xl border border-slate-800/80 print:bg-slate-50 print:border-slate-300 space-y-4">
                <div className="border-b border-slate-800 pb-2 mb-2">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="w-2.5 h-2.5 rounded-full bg-[#7F4F9F]" />
                    <h2 className="text-sm font-black uppercase tracking-wider text-white print:text-black">2. External Partnership</h2>
                  </div>
                  <p className="text-[11px] text-slate-400 print:text-slate-600">
                    We build trust through clarity, accountability, and professionalism.
                  </p>
                </div>

                <div className="space-y-4">
                  {PLAYBOOK_DATA.external.principles.map((p, idx) => (
                    <div key={p.id} className="space-y-1.5">
                      <div className="flex gap-2 items-start">
                        <span className="text-[#7F4F9F] font-bold text-xs">{idx + 1}.</span>
                        <h3 className="text-xs font-bold text-white print:text-black leading-tight">
                          {p.title}
                        </h3>
                      </div>
                      <p className="text-[10px] text-slate-400 print:text-slate-600 pl-4 leading-relaxed italic">
                        {p.desc}
                      </p>
                      <ul className="pl-4 space-y-1">
                        {p.practices.map((prac, i) => (
                          <li key={i} className="text-[10px] text-slate-300 print:text-slate-700 flex items-start gap-1">
                            <span className="text-[#7F4F9F]/80 shrink-0">•</span>
                            <span>{prac}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>

              {/* Column 3: Lead & Enable Others */}
              <div className="bg-slate-950/60 p-5 rounded-xl border border-slate-800/80 print:bg-slate-50 print:border-slate-300 space-y-4">
                <div className="border-b border-slate-800 pb-2 mb-2">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                    <h2 className="text-sm font-black uppercase tracking-wider text-white print:text-black">3. Lead and Enable</h2>
                  </div>
                  <p className="text-[11px] text-slate-400 print:text-slate-600">
                    We create the conditions for our people and teams to thrive.
                  </p>
                </div>

                <div className="space-y-4">
                  {PLAYBOOK_DATA.leadership.principles.map((p, idx) => (
                    <div key={p.id} className="space-y-1.5">
                      <div className="flex gap-2 items-start">
                        <span className="text-emerald-400 font-bold text-xs">{idx + 1}.</span>
                        <h3 className="text-xs font-bold text-white print:text-black leading-tight">
                          {p.title}
                        </h3>
                      </div>
                      <p className="text-[10px] text-slate-400 print:text-slate-600 pl-4 leading-relaxed italic">
                        {p.desc}
                      </p>
                      <ul className="pl-4 space-y-1">
                        {p.practices.map((prac, i) => (
                          <li key={i} className="text-[10px] text-slate-300 print:text-slate-700 flex items-start gap-1">
                            <span className="text-emerald-500/80 shrink-0">•</span>
                            <span>{prac}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>

            </div>

            {/* Poster Footer Info */}
            <div className="flex flex-col sm:flex-row items-center justify-between text-slate-500 border-t border-slate-800/60 pt-6 text-[11px]">
              <div>Iris.ai Culture Playbook — Core Guidelines Sheet</div>
              <div className="mt-2 sm:mt-0 italic">"We don't change our values based on context. We adapt how we express them."</div>
            </div>

          </div>
        )}

      </main>

      {/* Persistent global footer with direct link */}
      <footer className="border-t border-slate-900 mt-20 pt-8 pb-12 bg-slate-950/50 print:hidden text-center">
        <div className="max-w-7xl mx-auto px-4 text-slate-500 text-xs space-y-2">
          <p>
            © 2026{' '}
            <a
              href="https://iris.ai/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#3C49CC] font-bold hover:underline"
            >
              Iris.ai
            </a>
            . Built in alignment with the official Culture Playbook & Guiding Principles.
          </p>
          <p className="text-[11px] text-slate-600">The goal is to build meaningful technology, collaborate with integrity, and grow together.</p>
        </div>
      </footer>

    </div>
  );
}