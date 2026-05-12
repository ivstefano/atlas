# Engagement migration protocol (for the A4 rollout subagents)

You are migrating ONE engagement from the old flat folder `~/Documents/Axion/scoping/<company>/`
into the new structure at `~/Documents/engagements/<company>/`. Heineken
(`~/Documents/engagements/heineken/`) is the worked example — **read all of it first**
(`CONTEXT.md`, `STATUS.md`, `SOURCES.md`, `COMMERCIAL.md`, the stage folders, `_legacy/`) — it is
the gold standard for shape, tone, and depth. The plan this implements is `~/Documents/atlas/ENGAGEMENT_PLAN.md`
(read §0, §3, §4 — the structure, the lazy-creation rule, the four-file spec). Templates are in
`~/Documents/engagements/_template/`. IRIS people names/nicknames/roles: `~/Documents/atlas/_iris_people.md` (read it — transcripts mislabel speakers).

## Hard rules

1. **COPY, never move.** `~/Documents/Axion/scoping/<company>/` must be left untouched. Use `cp`.
2. **Do NOT run `git add` or `git commit`.** The parent does one commit at the end. Just create files.
3. **Big binaries do NOT go in the engagements repo.** The `.gitignore` already excludes `*.pdf *.zip
   *.xlsx *.docx *.pptx *.csv *.parquet` and `**/data/* **/raw/ **/processed/ **/results/ **/ground-truth/*
   **/sample-10pct/*` and `*credentials* *token* .env *.pem` and `.DS_Store __pycache__`. So:
   - Client data files (the actual PDFs/XLSX/XML the client sent, OCR/extraction output, large derived
     data, screenshots-by-the-hundred) → **leave them in Axion**. Reference them in `SOURCES.md` with an
     `AXION:` prefix path (e.g. `AXION:poc/extraction-week5/merged_results_v6.xlsx`) plus the future
     `s3://iris-engagements/<company>/{raw,processed,results,ground-truth}/` path.
   - Small generated `.docx`/`.xlsx`/`.pdf` deliverables that belong with the engagement (a SoW PDF, a
     scoping deck, an alignment doc) → you MAY `cp` them into the right stage folder; they'll sit in the
     working tree untracked (gitignored), referenced by path from `SOURCES.md`. That's fine and matches
     what was done for Heineken.
   - Credentials files → never copy. Note their Axion path in `SOURCES.md` under External, flagged "not
     migrated — → SSM/Secrets Manager".
4. **Markdown, transcripts (.txt/.md), small JSON, small .py extractor code → DO copy.** These are the
   context; git is their sync.
5. **Dates absolute.** Today is 2026-05-12. Use file mtimes (`stat -f '%Sm' -t '%Y-%m-%d' <file>`) and the
   transcripts to reconstruct the timeline.
6. **No em dashes are fine in prose but match Heineken's voice** — descriptive, factual, system-prompt
   style; commas/colons/parentheses over em dashes in `CONTEXT.md` per the plan §4. (STATUS/SOURCES/COMMERCIAL
   can be looser, like Heineken's.)

## What to build

```
~/Documents/engagements/<company>/
  CONTEXT.md       ← the stable picture. Header block (Stage / Type / Lead source / Introduced by / Aliases / Opened),
                     then the 8 sections from the template, filled the way Heineken's is. Type = axion-extraction /
                     rag / hybrid / TBD. §4 "what this client cares about" is the highest-value part — the 2-3 things
                     only in Ivo's head. §5 Data — what exists, where, format, quality, access status, the gotchas.
                     §6 stakeholders table (client business-owner/SME/manager + the IRIS people on the calls). §7
                     current phase + what "done" means.
  STATUS.md        ← append-only, newest on top. One entry per meaningful event reconstructed from the transcripts +
                     docs + mtimes. Top entry dated 2026-05-12: "engagement migrated into the new structure..." like
                     Heineken's. Then one entry per call/milestone/decision going back. Reference the transcript path
                     in each entry's Notes line.
  SOURCES.md       ← every artifact, one line each, with "this sheet/section is the one that matters" notes. Sections:
                     Canonical / Meeting notes & transcripts / Data samples & client files (with AXION: paths) /
                     Generated artifacts / Contracts / External. Mirror Heineken's SOURCES.md structure.
  COMMERCIAL.md    ← the Jordan/sales side: deal stage, lead source, pricing (scoping free? PoC €X/Yw? implementation?),
                     commercial gate, contract status (NDA / SoW — drafted/sent/signed?), negotiation notes. If the
                     folder has a SoW/proposal, mine it. HubSpot deal: "not on file / MCP not wired" unless there's a link.
  <stage folders, lazily — only the stages this engagement has actually reached>:
    1_pre-scoping/   transcripts/  notes.md      ← intro / pre-scoping / tech-Q&A call transcripts
    2_scoping/       transcripts/  notes.md  data/(.gitkeep)  extraction/(if axion-type: harness/extractor code)  + the scoping deliverable (.md/.html/.docx) if there is one
    3_contracting/   transcripts/  notes.md  contracts/  ← NDA/SoW working copies + the SoW .pdf/.md
    4_poc/           transcripts/  notes.md  data/(.gitkeep)  sample-10pct/ ground-truth/ eval/ (if axion-type)  + poc deliverables
    5_implementation/ transcripts/  notes.md  handoff.md  ← only if it's reached implementation
  _legacy/         ← everything from the old flat folder that doesn't have a clean home in the new structure, copied
                     wholesale (the old top-level .md files, abandoned exploration code, etc.). Referenced from SOURCES.md.
  _briefs/.gitkeep ← empty, for the future meeting-prep loop.
```

- Empty `transcripts/`, `data/` dirs that you want git to track → put a `.gitkeep` in them.
- If a stage was skipped (e.g. no separate scoping presentation — went straight to PoC), don't create that
  stage folder; note the skip in STATUS.md.
- `notes.md` in each stage folder = a few sentences of working notes for that stage, like Heineken's.

## Process

1. Read Heineken's `engagements/heineken/` fully. Read `_template/`. Read `atlas/_iris_people.md` and skim `atlas/ENGAGEMENT_PLAN.md` §0/§3/§4.
2. `find ~/Documents/Axion/scoping/<company>/ -type f -not -name .DS_Store` and `stat` the files for dates.
3. Read every `.md` and `.txt` transcript in the folder (these carry the story). Skim the larger docs (.docx
   you can't easily read — note them by name/date). Figure out: client, use case, type (axion/rag/hybrid),
   current stage, the stakeholders, the data, what the client cares about, the timeline, the commercial state.
4. Build the folder per the structure above. COPY the files that should be copied; leave binaries in Axion and
   reference them with `AXION:` paths.
5. Write the four core files. Match Heineken's depth — these should let a tech person start the work cold.
6. **Do not commit.** When done, report back to the parent: a one-paragraph summary of the engagement, its
   stage and type, which stage folders you created, what you left in Axion, and any open questions / things
   you couldn't determine.
