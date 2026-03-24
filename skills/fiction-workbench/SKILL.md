---
name: fiction-workbench
description: Structured workflow for long-form fiction using a bible and manuscript chapter structure. Use for drafting, editing, critique, or continuity sealing while preserving voice, canon, and narrative direction.
argument-hint: <write|edit|critique|seal> <chapter-file>
disable-model-invocation: true
---

Treat the human as the author. Your job is to reduce drift, preserve intent, and improve discipline across a long-form fiction project.

Parse the invocation arguments like this:

- Mode: `$0`
- Target chapter or scene file: `$1`

If either is missing, ask one short clarifying question and stop.

## Before You Start

1. Read the target file first.
2. Assume the project uses this structure:
   - `bible/characters/`
   - `bible/locations/`
   - `bible/themes/`
   - `bible/emotional-arc.md`
   - `bible/style-guide.md`
   - `bible/narrative-spine.md`
   - `manuscript/chapters/`
3. Read `bible/style-guide.md`, `bible/narrative-spine.md`, and `bible/emotional-arc.md` when they exist.
4. Read the relevant files under `bible/characters/`, `bible/locations/`, and `bible/themes/` based on the target chapter.
5. When useful for continuity, read adjacent files in `manuscript/chapters/`.
6. Do not assume canon that is not present in the source files.

## Global Rules

- Preserve established voice, chronology, and character integrity.
- Preserve the project’s existing spelling and punctuation conventions.
- Prefer concrete, grounded prose over abstract explanation.
- Remove generic AI phrasing, theatrical dialogue, and empty literary flourish.
- Do not introduce new lore, backstory, motifs, or symbolic systems unless the source material supports them.
- Do not flatten deliberate ambiguity or overexplain subtext.
- Keep output aligned with the mode requested.

## Mode: `write`

Use this mode to draft, expand, or rewrite the target chapter or scene.

Instructions:

- Apply the style guidance and narrative constraints from the project bible.
- Preserve the intended events, relationships, and emotional direction unless the user asks for structural changes.
- Strengthen pacing, scene grounding, and sensory specificity.
- End with forward movement or meaningful narrative pressure.
- If editing the file directly is appropriate in the current session, update the target file. Otherwise return the revised draft only.

Output:

- Revised draft only, unless the user explicitly asks for commentary.

## Mode: `edit`

Use this mode for line-level refinement without changing story intent.

Instructions:

- Improve rhythm, clarity, precision, and flow.
- Cut repetition, stiffness, and overwritten phrasing.
- Preserve meaning, scene order, and voice.
- If editing the file directly is appropriate in the current session, update the target file. Otherwise return the edited text only.

Output:

- Edited version only, unless the user explicitly asks for notes.

## Mode: `critique`

Use this mode for literary and structural feedback only.

Instructions:

- Do not rewrite unless the user explicitly asks for it after the critique.
- Evaluate voice consistency.
- Evaluate character integrity.
- Evaluate pacing and scene balance.
- Evaluate thematic alignment with `bible/narrative-spine.md`.
- Identify canon drift, false notes, artificial phrasing, and missed grounding opportunities.
- Be specific and direct.

Output format:

- What is working
- What feels false or weak
- What drifted from canon
- What to strengthen next

## Mode: `seal`

Use this mode when a chapter is finished and needs continuity notes.

Generate:

1. A concise chapter summary of roughly 150 to 250 words
2. A short emotional state note for the primary point-of-view character
3. Recurring motifs used in the chapter
4. Open threads carried forward
5. Drift warnings or continuity risks

Output rules:

- Keep it factual and compact.
- Do not invent future events.
- Return notes in chat unless the user explicitly asks you to write them into a continuity file.
