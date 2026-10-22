# Review Layers

Use for `lint` or the final diagnostic pass of a substantial revision. Scene and dialogue judgement do not wait for a clean mechanical scan. This workflow cannot certify literary quality.

## 1. Mechanical observations

Check typos, malformed annotations, accidental duplicate text and actual punctuation errors against the manuscript's conventions. Mixed straight and curly quotation marks may be intentional between quoted documents and narration. Markdown line-ending spaces can be deliberate. A semicolon, em dash or ellipsis is not itself an error; apply explicit project preferences in context.

Keep copy-edits narrow. Do not use a punctuation correction to rewrite a strong sentence.

## 2. Repetition and passage shape

Optionally run the read-only helper, using the Python available in the environment:

```sh
python3 scripts/repetition_scan.py /absolute/path/to/chapter.md --reference /absolute/path/to/approved-excerpt.md
```

Resolve `scripts/` relative to this skill directory. It emits JSON with counts, line locations and local clusters. It never edits files and makes no semantic verdict. It counts the supplied documents, including fictional ads or quoted dialogue, so read each match in its register. Extract matched passages for comparison where useful. A whole grief chapter is not a controlled baseline for a short family conversation.

The phrase scan stays within paragraphs and sentence punctuation, ignores frontmatter, headings and fenced code, and retains contractions. Its lexical families are deliberately approximate. A body-word hit may describe clothing; a glance may orient the scene. Numbers per thousand words aid comparison only; they are not acceptance limits. A shorter report can still describe worse prose.

Inspect [the watchlist](forbidden_patterns.md) for functional questions. Independently examine paragraph endings, gesture-separated dialogue, repeated setup–correction–payoff exchanges and triadic cadence. A regex cannot reliably recognise these larger patterns.

For an explicitly active hard-constraint profile, also use the checker in [constrained drafting](constrained-drafting.md). Its pass/fail result applies only to literal constraints. The repetition scanner remains advisory.

## 3. Literary review

Read the scene continuously and compare a sustained passage with the approved reference. Separate:

- **Coherence:** who knows what, chronology, physical continuity, motivation and consequences. Keep deliberate ambiguity.
- **Dialogue:** local motives, replies that develop, independent interests, purposeful actions and natural variation in turn length.
- **Emotion and narration:** earned inference, useful telling, particular desire, contradictions and the cost of what happens.
- **Form:** paragraph movement, selective imagery, compression versus scene time, overexplaining and repeated cadence.

For an actionable finding, quote or locate the passage, describe its reader effect and identify a repair. Do not report a weakness solely because a model's benchmark profile lists it.

## Output and revision

Prioritise consequential findings. Mark **keep**, **watch** and **revise** only when useful. A no-change judgement is legitimate. For requested critique, include strengths whose removal would make the passage worse.

After a repair, check the passage again for altered facts and voice. Do not rerun style passes indefinitely or announce that a chapter is “slop-free”. Distinguish an observed improvement from a hypothesis requiring the author's response.
