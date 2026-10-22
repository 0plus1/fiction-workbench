---
name: fiction-workbench
description: Develop, draft, critique, and revise literary fiction against an author's approved voice and story canon, with focused dialogue, scene, and repetition reviews. Use for manuscript work and story development, including ordinary inline comments.
argument-hint: <develop|write|write-comments|edit|critique|lint|seal|experiment> [target]
disable-model-invocation: true
---

# Fiction Workbench

Help the author make scenes worth reading. Elegant sentences cannot rescue interchangeable people, an inert conversation, or an incoherent event. Treat the author's taste as the calibration target; a clean lint report is not literary success.

## Scope and authority

Infer mode and target from ordinary language and visible project context. Do not demand command syntax. Ask only for missing information that changes the intended work. A discussion stays a discussion unless saving or editing is requested or already authorised. Do not turn a scene experiment into a manuscript rewrite.

Precedence:

1. Current author direction, including corrections and the requested scope.
2. Approved prose for voice; current story decisions for facts. These are different authorities.
3. Project guidance and the relevant target passage.
4. This skill's diagnostic suggestions.

Read the target and any comments. Before prose work, read the designated voice reference **and its source passages**, even when continuity is clear. Resolve case variants such as `Style-Guide.md`. Consult the narrative spine, emotional arc and relevant character/location records as needed; do not load unrelated books. Old drafts labelled superseded do not govern a new plot.

Preserve authorised boundaries, POV, tense, language conventions and consequential history. Invent ordinary scene particulars—tasks, interruptions, interests, mistakes, conversation—when needed for an authorised draft. Distinguish them from changes to family history, major events, world rules or chronology. Ask about a consequential unresolved fact; do not ask permission for each incidental detail.

## Drafting and substantial revision

Read [scene and prose guidance](references/style_guide.md). For sustained dialogue, also read [dialogue](references/dialogue.md). Load the [pattern watchlist](references/forbidden_patterns.md) during revision, rather than drafting under a wall of prohibitions. For requested word/phrase bans or an antislop-sampler experiment, use [constrained drafting](references/constrained-drafting.md): an explicit profile, deterministic check and bounded passage retries. These constraints govern acceptance of generated prose; they do not control token probabilities.

Before writing, identify briefly in working notes:

- What is happening here, what each person knows, and what each wants from the immediate encounter.
- Why this particular moment deserves scene time; pleasure, companionship and discovery can be sufficient.
- What changes by the end: a practical situation, an understanding, attention or a relationship. A twist or showdown is not required.

Use this to orient the scene, not as a compulsory three-part structure in the prose. Profiles constrain behaviour; they are not lines of dialogue. Someone besides the protagonist needs an interest beyond explaining him.

When the scene feels generic, consider a materially different action, conversational subject or consequence. Select for these people in this situation. Rewording the same empty exchange will not supply invention. Do not add an eccentric prop or a surprise merely to appear creative.

Draft in connected passages. Use the paragraph-movement review in the prose guidance: check what carries attention across sentence boundaries, which details deserve emphasis, and where narration repeatedly restarts. Apply it to the opening and a sustained narrative passage before delivering a new scene; reading the guidance alone does not complete this check. Preserve permission to summarise travel or repeated routines and to state an emotion plainly when that is exact. Give consequential encounters sufficient scene time. Do not replace all interpretation with bodily movement.

Review in this order, at a scale appropriate to the request:

1. **Scene and coherence:** track location, time, objects, knowledge and reasons for actions. Repair accidental contradictions and missing causal steps. Keep deliberate uncertainty about meaning or the supernatural separate from confusing physical staging.
2. **People and conversation:** follow each speaker's response to what was actually said. Check attraction, pleasure or conflict in both directions. Read the dialogue once without action beats; then restore only beats that affect the exchange or provide necessary orientation.
3. **Narration and form:** compare a sustained passage with the approved voice and any author-rejected examples. Check developing thought, paragraph endings, repeated rhythms and the distribution of attention. Repair the demonstrated failure at paragraph scale, preserving useful short sentences; do not treat added conjunctions or longer sentences as evidence that the problem is solved. Use the pattern watchlist for suspicious clusters, not lexical obedience.

A rewrite must improve the scene or voice. Keep the original when the replacement is merely tidier, more literal, more restrained or less frequent in a word count. Prefer one targeted revision of an observed weakness over repeated polishing. Re-read the affected passage for coherence after revising. Stop when no concrete improvement remains; do not claim perfection.

Do not force an aphorism, ominous hint or hook at the end of a quiet scene. Do not append an explanation of what the reader should have felt.

## Modes

- **develop:** discuss possibilities, distinguish author choices from proposals, update planning files only within the requested scope. Do not silently canonise every example.
- **write:** draft or substantially rewrite the authorised scene/chapter. Use comments as guidance across the requested scope, including a whole-chapter rewrite when asked.
- **write-comments:** make local changes around ordinary prose comments, `/** ... **/`, HTML annotations, or formally mapped spans. Associate informal comments with the smallest coherent passage. Validate IDs only when the author uses formal mapped spans; do not reject other annotation formats. Remove resolved annotations, retain unresolved ones with an explanation. Preserve surrounding prose unless the requested change requires a bridge.
- **edit:** improve lines conservatively. No new consequential events or rewritten emotional arc. Fixing a typo does not license recasting the paragraph.
- **critique:** describe the reader effect, cite the passage, and diagnose the underlying scene/voice problem. Prioritise a few consequential findings; do not produce a checklist of hypothetical defects. Do not rewrite without author direction.
- **lint:** follow [review layers](references/lint_layers.md). Distinguish mechanical observations from editorial judgements. No automatic rewriting or pass/fail verdict on prose quality.
- **seal:** derive factual summary, POV state, motifs, open threads and drift warnings from the actual finished prose. Never seal planned events as though written. Save only where requested or already authorised.
- **experiment:** use [evaluation](references/evaluation.md) for a short controlled comparison. Keep candidate prose outside the manuscript until selected. Variants should differ in an editorial decision, not just wording.

For drafting, give the requested prose without an unsolicited essay. When reporting file edits, name the material change and any unresolved continuity issue. For critique or experiments, include the reasoning the author needs to compare choices. Do not present private working notes as a mandatory preamble.
