#!/usr/bin/env python3
"""Read-only repetition observations for prose. Counts are not literary verdicts."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)*", re.UNICODE)
FAMILIES = {
    'gesture': set('glance glanced glances nod nodded nods grin grinned grins lean leaned leant leans crouch crouched crouches stare stared stares shrug shrugged shrugs fold folded folds'.split()),
    'body_detail': set('finger fingers wrist wrists forearm forearms sternum elbow elbows heel heels knee knees foot feet'.split()),
    'physiology': set('tighten tightened tightens tremble trembled trembles breathe breathed breathes loosen loosened loosens'.split()),
}
PHRASES = ('could not decide whether', 'could decide whether', 'stood close enough',
           'close enough to smell', 'spent twenty years', 'twelve years ago',
           'asked whether', 'ask whether', 'stood beside', 'sat beside', 'two fingers',
           'one hand', 'said nothing', 'neither moved', 'smiled without',
           'without touching', 'for the first time', 'the kind of', 'the sort of',
           'what mattered', 'the truth was')


def prose_paragraphs(text):
    """Retain original line numbers; discard YAML, headings and fenced code."""
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() in ('---', '...'):
                start = i + 1
                break
    groups, current, fence = [], [], None
    for index in range(start, len(lines)):
        line = lines[index]
        stripped = line.strip()
        boundary = re.match(r'^(`{3,}|~{3,})', stripped)
        if boundary:
            if current:
                groups.append(current)
                current = []
            marker = boundary.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        if not stripped or stripped == '>' or stripped.startswith('#') or stripped in ('***', '---', '___'):
            if current:
                groups.append(current)
                current = []
            continue
        current.append((index + 1, line))
    if current:
        groups.append(current)
    return groups


def inspect(path):
    groups = prose_paragraphs(path.read_text(encoding='utf-8'))
    all_tokens, runs = [], []
    for group in groups:
        run = []
        for line_number, line in group:
            cursor = 0
            for match in WORD.finditer(line):
                if re.search(r'[.!?;:]', line[cursor:match.start()]) and run:
                    runs.append(run)
                    run = []
                token = (match.group().casefold().replace('’', "'"), line_number)
                run.append(token)
                all_tokens.append(token)
                cursor = match.end()
            if re.search(r'[.!?;:]', line[cursor:]) and run:
                runs.append(run)
                run = []
        if run:
            runs.append(run)
    total = len(all_tokens)
    family_hits = {}
    clusters = []
    for name, vocabulary in FAMILIES.items():
        hits = [(index, token, line) for index, (token, line) in enumerate(all_tokens) if token in vocabulary]
        family_hits[name] = {
            'count': len(hits),
            'per_1000_words': round(len(hits) * 1000 / total, 2) if total else 0,
            'words': dict(Counter(token for _, token, _ in hits).most_common()),
            'first_locations': [{'line': line, 'word': token} for _, token, line in hits[:30]],
        }
        # Candidate retrieval threshold, not a recommended maximum for prose.
        last_end = -1
        for i, (index, _, line) in enumerate(hits):
            if index <= last_end:
                continue
            window = [h for h in hits[i:] if h[0] < index + 120]
            if len(window) >= 5:
                clusters.append({'family': name, 'start_line': line,
                                 'end_line': window[-1][2], 'hits': len(window)})
                last_end = window[-1][0]
    occurrences = defaultdict(list)
    for run in runs:
        words = [t for t, _ in run]
        for length in range(3, 7):
            for offset in range(len(run) - length + 1):
                occurrences[tuple(words[offset:offset+length])].append(run[offset][1])
    repeats = [(phrase, lines) for phrase, lines in occurrences.items() if len(lines) >= 3]
    repeats.sort(key=lambda item: (-len(item[1]), -len(item[0]), item[0]))
    selected = []
    for phrase, lines in repeats:
        # Prefer a longer repeated phrase when it covers the exact same occurrences.
        if any(lines == other_lines and any(phrase == other[i:i+len(phrase)] for i in range(len(other)-len(phrase)+1))
               for other, other_lines in selected):
            continue
        selected.append((phrase, lines))
        if len(selected) == 20:
            break
    watched = {}
    for phrase in PHRASES:
        needle = phrase.split()
        locations = []
        for run in runs:
            words = [t for t, _ in run]
            locations.extend(run[i][1] for i in range(len(run)-len(needle)+1) if words[i:i+len(needle)] == needle)
        if locations:
            watched[phrase] = {'count': len(locations), 'lines': locations[:30]}
    return {
        'path': str(path.resolve()), 'word_count': total,
        'lexical_families': family_hits, 'candidate_clusters': clusters[:20],
        'watched_phrases': watched,
        'repeated_phrases': [{'phrase': ' '.join(phrase), 'count': len(lines), 'lines': lines[:30]} for phrase, lines in selected],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    parser.add_argument('--reference', type=Path, action='append', default=[])
    args = parser.parse_args()
    try:
        result = {'notice': 'Read-only observations. No bans, score, auto-edits or literary pass/fail. Compare registers and sample sizes.',
                  'target': inspect(args.target), 'references': [inspect(p) for p in args.reference]}
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f'Cannot read input: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
