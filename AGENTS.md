<!-- antislop:start -->
## antislop
For UI, copy, people, mobile layout, or code comments work, read these installed skill files directly (use these paths even if a same-named global skill exists):
- Core filter, always on: `antislop`: `.agents/skills/antislop/SKILL.md`
- UI / visual: `antislop-ui`: `.agents/skills/antislop-ui/SKILL.md`
- Copy & text: `antislop-copywriting`: `.agents/skills/antislop-copywriting/SKILL.md`
- People: `antislop-human`: `.agents/skills/antislop-human/SKILL.md`
- Mobile / responsive: `antislop-layoutmobile`: `.agents/skills/antislop-layoutmobile/SKILL.md`
- Code comments: `antislop-code`: `.agents/skills/antislop-code/SKILL.md`
Before starting, follow the core's "Two Usage Modes" section in strict order: explicit session instruction first, then global preference, then ask. A session instruction always wins. For a resolved mode, say `antislop active: <mode> (session override).` or `antislop active: <mode> (global preference).` once before presenting findings or making edits, using the actual mode and source. Acknowledging the user's request without naming the source does not replace this notice.
Only an explicit choice of antislop during or after selects a session mode. A request to review, audit, or avoid file edits does not select a mode; read the global preference in that case. Another skill's mode does not select antislop's mode.
If the mode is unresolved, ask during/after and end the response; wait for the answer before any UI review, planning, or concept. For read-only tasks, put the active-mode notice only at the start of the final answer, never in progress messages. For editing tasks, announce before the first edit and omit it from the final answer.
To update antislop later: `npx antislop-ai --update`, or run `npx antislop-ai` and pick Overwrite them.

## IoT Learning Hub — Permanent Anti-Slop Policy
- Default mode: DURING (Permanent session & project rule).
- Scope: Seluruh level (Level 1–4, Chapter 01–40), specialization tracks, UI, UX, slide deck, diagram, dokumentasi, dan source code.
- Final audit: Mandatory setelah penyelesaian setiap level.
- Academic accuracy: Higher priority than aesthetics; technical depth, mathematical models, worked engineering examples, and empirical verification must take precedence.
- Engineering reproducibility: Mandatory; all code, simulation configs, and verification hashes must be reproducible and executable.
- Existing architecture preservation: Mandatory; maintain catalog structure, publication guards, Vite base handling, and test suites.
- No generic AI writing or UI patterns: Eliminate filler words, conversational meta-commentary, vague marketing claims, floating meaningless cards, and repetitive bullet lists.
- No repeated mode selection: DURING mode is permanently locked for all subsequent IoT Learning Hub phases.
<!-- antislop:end -->
