# Constrained Drafting and Passage Retries

Use when the author requests word/phrase banning, antislop-sampler-like behaviour, or a constrained prose experiment. This is an opt-in mode for the authorised new or rewritten passage, not a retroactive restriction on the book. Ordinary drafting still uses the contextual watchlist.

## Mechanism and limits

Inspired by [AntiSlop Sampler](https://github.com/sam-paech/antislop-sampler), whose README describes matching unwanted strings, backtracking and adjusting token probabilities before continuing generation. It also recommends a curated list rather than blindly adopting its supplied corpus-derived list.

This skill supplies a draft/check/rewrite loop at passage scale. It does not access logits, adjust sampling weights, implement token-level backtracking or reproduce that sampler's output distribution. Hard constraints restrict which drafts can be accepted; review entries ask for an editorial decision. Neither is a measured probability penalty. Do not claim improved creativity or detector scores from lower word counts.

## Choose a scoped profile

Use an author-supplied list when available. Otherwise use [the bundled cross-model profile](constraint-profile.json) for requested constrained drafting. Its hard bans are generated from EQBench Creative Writing v3 entries listed by at least 10% of models within any one category: words, phrases, bigrams or trigrams. Each model contributes one vote per entry, regardless of its output length or reported occurrence count. The profile records its source snapshot, selection threshold and category evidence. The repository's root-level `generate_constraint_profile.py` rebuilds it from downloaded profiles; the generator is development tooling, not part of this installed skill. Preserve the author's ability to change or remove constraints.

- `hard`: literal words/phrases excluded from the generated prose under this profile. A match requires another attempt; do not silently waive it because the sentence seems good.
- `review`: literal words/phrases worth inspecting. Keep an occurrence that earns its place; otherwise retry the passage. These are not forbidden and have no numerical weight.

Names, necessary technical terms, the book's recurring objects, ordinary speech tags and quoted source material should not accidentally become collateral bans. Check the profile against the intended scene before drafting. If an explicit author ban conflicts with a required fact or quotation, state the conflict rather than deleting the fact or pretending the ban was met. Apply checking only to the authorised generated span; extract it to a temporary file when the surrounding chapter contains approved text.

The generated profile uses literal EQBench entries, including names, ordinary words and n-grams that may omit connecting words. It does not infer missing words or grammatical variants. Case and apostrophe variants are merged; punctuation remains. Metadata is evidence, not an extra set of constraints. Every `hard` entry is enforced when the profile is active; `review` is empty in the generated profile. Ordinary drafting still uses the contextual watchlist.

## Draft, check, reconsider

1. Draft from the scene's action, people and approved voice with the active hard constraints in view. Leave room for an unexpected association or a different action; do not compose a list of synonyms in advance.
2. Run the checker below on the candidate. For each hard match, return to the smallest passage where a different choice is possible, usually the sentence or paragraph containing it. Establish what the passage needs to accomplish, then write it again with the constraint. A local lexical change is sufficient when it is genuinely the better sentence; do not default to euphemisms for the same stock gesture.
3. Inspect review matches in context. A cluster can justify reconsidering an exchange; a single necessary gesture can stay. Apply the existing paragraph and dialogue reviews even when there are no lexical matches. The Anglesea opening's rhythm problem would not be solved by this profile alone.
4. Check the revised candidate for constraints and then for changes to facts, meaning, voice and physical continuity. Re-read adjacent paragraphs so a local retry does not break the scene. Use at most two repair rounds per passage. If a hard conflict remains, report the candidate as failing the constraint; do not silently relax the list or claim completion. A return to ordinary drafting requires author direction when hard bans were explicitly requested.

When editing manuscript prose, use a temporary candidate until it meets the active hard constraints and preserves the scene. Save only within the user's authorised scope. A mechanically clean candidate remains a literary draft for the author to judge.

## Deterministic check

Resolve both script and profile paths relative to this skill directory:

```sh
python3 scripts/constraint_check.py /absolute/path/to/candidate.md --profile references/constraint-profile.json
```

The checker is read-only. JSON output contains matched strings, original line numbers and paragraph boundaries. Exit status 0 means no hard matches (review matches may remain); 1 means hard matches; 2 means an input error. This is a constraint check, not a literary score.

Matching is case-insensitive, uses whole-word boundaries around literal entries, accepts whitespace between phrase words and both straight and curly apostrophes. It skips Markdown frontmatter, headings and fenced code, and does not cross paragraph boundaries. It does not stem words or infer grammatical patterns: banning `trembled` does not ban `trembling`. List intended inflections explicitly; do not evade the spirit of the constraint by changing only an inflection. Dialogue and blockquotes within the checked prose are included. Arbitrary regex bans are not supported by this checker.

## Evaluate the effect

For an author-requested comparison, use the same scene brief and voice reference with and without the selected constraints; keep both candidates outside the manuscript until selection. Assess naturalness, invention, paragraph movement, emotional precision and fidelity as well as matches. A forced circumlocution is a cost even if the banned term disappears. A single comparison cannot establish that the overall statistical distribution improved; describe the observed differences in the actual passages.
