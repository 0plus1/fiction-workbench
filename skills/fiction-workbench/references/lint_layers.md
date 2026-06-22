# Fiction Lint Layers

Use this file for anti-slop linting. Keep lint separate from drafting: the prose pass writes the scene; the lint pass catches mechanical and structural tells after the text exists.

Treat these checks as conservative editorial signals. A match is a prompt to inspect the line, not automatic proof that the prose is bad.

## Layer 1: Surface

Use pure grep-style checks for mechanical habits. Report counts by chapter plus line-numbered examples when a cap is exceeded.

| Rule ID | Check | Default |
| --- | --- | --- |
| `surface.em_dash_count` | Count em dashes. | Flag above 5 per chapter. |
| `surface.ellipsis_count` | Count ellipses. | Flag above 3 per chapter. |
| `surface.ellipsis_beat` | `...` used as an emotional beat. | Forbidden; prefer action beat. |
| `surface.semicolon_dialogue` | Semicolon inside quoted dialogue. | Usually flag. |
| `surface.double_space` | Double spaces between words or after punctuation. | Flag all. |
| `surface.quote_consistency` | Mixed straight and smart quotes in the same file. | Flag mixed style only. |
| `surface.fragment_stack` | Three or more one-to-five-word sentences close together. | Flag cluster. |

Suggested regex seeds:

```text
surface.em_dash_count: —
surface.ellipsis_count: \.\.\.|…
surface.semicolon_dialogue: ["'][^"'\n]*;[^"'\n]*["']
surface.double_space: [^\n] {2,}[^\n]
surface.smart_double_quote: [“”]
surface.straight_double_quote: "
surface.smart_single_quote: [‘’]
surface.straight_single_quote: '
```

## Layer 2: Structural

Use regex with a few words of context. These catch the sentence shapes, vague lexical placeholders, and reader-directed nudges where generic AI voice often lives.

| Rule ID | Pattern | Suggested Move |
| --- | --- | --- |
| `struct.not_x_its_y` | `not X, it is Y`; `not X, it's Y`; `wasn't just X, it was Y` | State the point directly or show the distinction in action. |
| `struct.not_x_dash_y` | `wasn't just X -- it was Y`; `wasn't just X - it was Y` | Remove the reveal scaffold. |
| `struct.three_fragment_punch` | `X. Not Y. Z.` or `Not X. Not Y. Just Z.` | Recombine into normal prose. |
| `struct.testament_symphony_dance` | `a testament to`, `a symphony of`, `a dance of` | Replace abstract flourish with concrete description. |
| `struct.chapter_ending_aphorism` | `and that, more than anything, was what...`; `that was what he would remember` | End on action, image, pressure, or consequence. |
| `struct.in_that_moment_realized` | `in that moment, he/she/they realized/knew/understood` | Put the realization into perception or choice. |
| `struct.adverb_stack` | Two adverbs around a speech or action tag. | Keep the one that changes meaning, or replace with action. |
| `struct.vague_quality` | `quality of X`, `a particular quality`, `qualitatively` used as blur. | Name the property, convert it to a verb, or cut it. |
| `struct.placeholder_something` | Clustered `something`, or `doing something that...` where a real verb belongs. | Name the thing, recast with a concrete verb, or keep only deliberate unknowability. |
| `struct.reader_attention_nudge` | `worth pausing on`, `worth noting`, `worth holding onto`, `this bears repeating`, `what is striking here`. | Cut the meta-layer and make the point directly. |

Suggested regex seeds:

```text
struct.not_x_its_y: \b(?:it\s+)?(?:is|was|wasn['’]t|isn['’]t)\s+not\s+[^.!?\n,;:]{1,80},?\s+(?:it\s+)?(?:is|was|it['’]s)\s+[^.!?\n]{1,120}
struct.not_x_dash_y: \bwasn['’]t\s+just\s+[^.!?\n—-]{1,80}\s+[—-]\s+(?:it\s+)?was\s+[^.!?\n]{1,120}
struct.three_fragment_punch: \b(?:Not|No)\s+[^.!?\n]{1,30}\.\s+(?:Not|No)\s+[^.!?\n]{1,30}\.\s+(?:Just\s+)?[^.!?\n]{1,60}\.
struct.testament_symphony_dance: \ba\s+(?:testament\s+to|symphony\s+of|dance\s+of)\b
struct.chapter_ending_aphorism: \b(?:and\s+)?that,\s+more\s+than\s+anything,\s+was\s+what\b|\bthat\s+was\s+what\s+(?:he|she|they)\s+would\s+remember\b
struct.in_that_moment_realized: \bin\s+that\s+moment,\s+(?:he|she|they|[A-Z][a-z]+)\s+(?:realized|knew|understood)\b
struct.adverb_stack: \b\w+ly,\s+(?:almost\s+)?\w+ly\b|\bsaid\s+\w+ly,\s+(?:almost\s+)?\w+ly\b
struct.vague_quality: \b(?:the\s+)?quality\s+of\b|\ba\s+(?:particular|certain|strange|special)\s+quality\b|\bqualitatively\b
struct.placeholder_something: \bdoing\s+something\s+that\b|\bsomething\s+(?:more|previously|real|structural|different|else)\b|\bsomething\b.{0,80}\bsomething\b
struct.reader_attention_nudge: \b(?:is|was|seems|felt)?\s*worth\s+(?:pausing\s+on|noting|holding\s+onto|remembering)\b|\bthis\s+bears\s+repeating\b|\bwhat\s+is\s+striking\s+here\s+is\b
```

False-positive notes:

- `struct.vague_quality`: allow genuine terms of art such as `occult quality` or cases where `qualitatively` marks a real category distinction.
- `struct.placeholder_something`: allow deliberate unknowability, mystery, or point-of-view limitation. Flag clusters and lazy verb avoidance first.
- `struct.reader_attention_nudge`: allow rare essayistic voice only if the narrator's established style addresses the reader directly.

## Layer 3: Semantic

Use agent judgment only after Layer 1 and Layer 2 are stable. Keep lenses separate so one kind of concern does not contaminate the others.

- Style lens: telling emotion instead of showing it, repeated abstraction, overexplained subtext, same paragraph arc repeated.
- Character lens: lines or choices that contradict the character's established voice sample, wants, boundaries, or level of self-knowledge.
- Plot lens: scene beats that do not change pressure, stakes, options, or information.
- Continuity lens: contradiction with relevant bible files, adjacent chapters, timeline, location logic, or open threads.

Output line-numbered evidence when possible. For semantic findings, include the reasoning path briefly, because these are not deterministic.

## Add Rules Over Time

Add Layer 2 rules only after seeing the pattern recur in real drafts. Store them with:

- rule ID
- regex seed
- example match
- false-positive note
- preferred rewrite move
