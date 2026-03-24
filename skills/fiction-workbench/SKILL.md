---
name: fiction-workbench
description: Canon-aware drafting, line editing, critique, and continuity sealing for long-form fiction projects organized around chapter files plus a story bible. Use when working on a specific scene or chapter and needing to preserve voice, chronology, character integrity, motifs, and narrative direction.
argument-hint: <write|edit|critique|seal> <chapter-file>
disable-model-invocation: true
---

Treat the human as the author. Your job is to reduce drift, preserve intent, and improve discipline across a long-form fiction project.

Parse the invocation arguments like this:

- Mode: `$0`
- Target chapter or scene file: `$1`

If either is missing, ask one short clarifying question and stop.
If the mode is not `write`, `edit`, `critique`, or `seal`, explain the valid modes briefly and stop.

## Workflow

1. Read the target file first.
2. Use this project structure when the files exist:
   - `bible/characters/`
   - `bible/locations/`
   - `bible/themes/`
   - `bible/emotional-arc.md`
   - `bible/style-guide.md`
   - `bible/narrative-spine.md`
   - `manuscript/chapters/`
3. Read `bible/style-guide.md`, `bible/narrative-spine.md`, and `bible/emotional-arc.md` when they exist.
4. Read only the character, location, and theme files that are clearly relevant to the target chapter or scene.
5. Read adjacent chapter files only when continuity, chronology, or payoff depends on them.
6. Work from the text that exists. Do not invent canon, backstory, or symbolism that the files do not support.

## Global Rules

- Preserve established voice, chronology, and character integrity.
- Preserve the project’s existing spelling and punctuation conventions.
- Preserve point of view, tense, and markdown structure unless the user asks for a change.
- Prefer concrete, grounded prose over abstract explanation.
- Remove generic AI phrasing, theatrical dialogue, and empty literary flourish.
- Do not introduce new lore, backstory, motifs, or symbolic systems unless the source material supports them.
- Do not flatten deliberate ambiguity or overexplain subtext.
- Prefer the smallest amount of canon lookup needed to do the job well.
- Keep output aligned with the mode requested.

## Mode: `write`

Use this mode to draft, expand, or rewrite the target chapter or scene.

- Apply the style guidance and narrative constraints from the project bible.
- Preserve the intended events, relationships, and emotional direction unless the user asks for structural changes.
- Strengthen pacing, scene grounding, and sensory specificity.
- Resolve local awkwardness, but do not quietly change story logic or scene outcomes.
- End with forward movement or meaningful narrative pressure.
- If editing the file directly is appropriate in the current session, update the target file. Otherwise return the revised draft only.

Output:

- Revised draft only, unless the user explicitly asks for commentary.

## Mode: `edit`

Use this mode for line-level refinement without changing story intent.

- Improve rhythm, clarity, precision, and flow.
- Cut repetition, stiffness, and overwritten phrasing.
- Preserve meaning, scene order, and voice.
- Avoid adding new beats, new lore, or new motivations.
- If editing the file directly is appropriate in the current session, update the target file. Otherwise return the edited text only.

Output:

- Edited version only, unless the user explicitly asks for notes.

## Mode: `critique`

Use this mode for literary and structural feedback only.

- Do not rewrite unless the user explicitly asks for it after the critique.
- Evaluate voice consistency.
- Evaluate character integrity.
- Evaluate pacing and scene balance.
- Evaluate thematic alignment with `bible/narrative-spine.md`.
- Identify canon drift, false notes, artificial phrasing, and missed grounding opportunities.
- Cite concrete problem spots when possible.
- Be specific and direct.

Output headings:

- `What is working`
- `What feels false or weak`
- `What drifted from canon`
- `What to strengthen next`

## Mode: `seal`

Use this mode when a chapter is finished and needs continuity notes.

Generate these sections:

1. `Summary`: roughly 150 to 250 words
2. `POV State`: the primary point-of-view character's emotional position at the end of the chapter
3. `Motifs`: recurring images, symbols, or phrases actually used in the chapter
4. `Open Threads`: unresolved tensions, promises, or continuity hooks carried forward
5. `Drift Warnings`: continuity risks, canon pressure points, or details likely to cause later contradiction

Output rules:

- Keep it factual and compact.
- Do not invent future events.
- Return notes in chat unless the user explicitly asks you to write them into a continuity file.
