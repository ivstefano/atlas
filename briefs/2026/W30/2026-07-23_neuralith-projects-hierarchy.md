# Neuralith Playground / Projects — system hierarchy

Source: Playground Design Next Steps, 2026-07-23 (Ivo, Vankata, Dezea Studio).

## Project object hierarchy

```mermaid
graph TD
    P[Project]

    P --> D[Dataset]
    P --> O[Output / ODL<br/>one table across the whole dataset]

    D --> F[File]
    F --> A[Artifact<br/>per-file derived view]

    F -.rows.-> O

    classDef undef fill:#fff3cd,stroke:#d39e00
    class O undef
```

Reading: a Project holds a Dataset of Files, each File yields an Artifact. The Output (ODL) hangs off the Project, not off any single File: it is one table for the whole dataset, where each File contributes one or more rows.


## Data model behind the ODL view

```mermaid
graph LR
    D[Client documents<br/>PDFs, mixed languages] --> E[Extraction]
    E --> ODL[ODL<br/>one big table<br/>schema is per-client]
    ODL --> A1[Client delivery<br/>full table, all columns<br/>fed into their analytics]
    ODL --> A2[Playground view<br/>curated subset<br/>tells a story]
    ODL -.future.-> A3[Reconstructed document<br/>text output, not table]

    classDef future fill:#eee,stroke:#999,color:#666
    class A3 future
```

## What needs to happen

```mermaid
graph TD
    T1[Ivo: produce dummy demo table<br/>pick columns that tell the story] --> T2[Vankata: confirm story]
    T2 --> T3[Dezea: build ODL preview component]
    T4[Dezea: post upload-flow wireframes<br/>in channel] --> T5[Review async<br/>Dezea off next week]
    T6[Vankata: map user types<br/>3-4 max, transitions between them] --> T7[Decides where<br/>Create Project lives]
    T7 --> T3
    T8[Ivo: reissue platform access link<br/>expired after 3 days] --> T3

    classDef ivo fill:#d1e7dd,stroke:#0f5132
    classDef van fill:#cfe2ff,stroke:#084298
    classDef dez fill:#f8d7da,stroke:#842029
    class T1,T8 ivo
    class T2,T6 van
    class T3,T4 dez
```

## Key constraints (from Vankata)

- Playground ODL view is a **showcase, not a tool**. No column manipulation, no expand/collapse. Wow moment on first screen.
- Client-facing ODL (Aumovio) is **not** the design ground truth. Playground needs something simpler.
- ODL schema is per-client. UI must be generic; Ivo picks which columns/values surface per dataset.
- ODL preview reuses the **same component** as the existing artifact preview, different artifact type.
- Project request is one-time in V1. Edit means propagating changes to Ivo mid-scoping — deferred.
- Playground → Create Project is gated on payment. Button may be hidden for unpaid users.

## Open questions

- Which user type lands where after registration? Real sales-pipeline clients go straight to Projects, demo users to Playground — but no map exists yet.
- Column clustering (Aumovio grouped view): Vankata says too complex for playground, relevant for real clients. Where does it land?
- Are the 5-8 pre-scoping questions written down anywhere, or does Ivo draft them?
- ArcelorMittal data is harder to make impressive at a glance. Is Aumovio the demo dataset?
